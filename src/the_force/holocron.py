"""Holocron module - personal wisdom journal with persistent storage."""

import json
import os
from datetime import datetime
from typing import Optional


class HolocronError(Exception):
    """Exception raised for Holocron validation errors."""
    pass


class Holocron:
    """Personal wisdom journal with persistent JSON storage."""
    
    def __init__(self, db_path: str):
        """Initialize Holocron with storage at given path.
        
        Args:
            db_path: Path to JSON file for storing entries
        """
        self.db_path = db_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage file exists and is valid JSON."""
        if not os.path.exists(self.db_path):
            self._save_data({"entries": []})
            return
        
        # Try to load existing data
        try:
            with open(self.db_path, 'r') as f:
                data = json.load(f)
            # Validate structure
            if not isinstance(data, dict) or 'entries' not in data:
                raise ValueError("Invalid holocron structure")
        except (json.JSONDecodeError, ValueError):
            # Corrupted file, reinitialize
            self._save_data({"entries": []})
    
    def _load_data(self) -> dict:
        """Load data from storage file."""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is missing or corrupted, return empty
            return {"entries": []}
    
    def _save_data(self, data: dict):
        """Save data to storage file."""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _next_id(self) -> int:
        """Get next available ID."""
        data = self._load_data()
        if not data['entries']:
            return 1
        return max(entry['id'] for entry in data['entries']) + 1
    
    def add_entry(self, text: str, source: str = "") -> int:
        """Add a wisdom entry to the holocron.
        
        Args:
            text: The wisdom text
            source: Optional source/author of the wisdom
            
        Returns:
            ID of the newly created entry
            
        Raises:
            HolocronError: If text is empty or whitespace-only
        """
        if not text or not text.strip():
            raise HolocronError("Wisdom text cannot be empty")
        
        entry_id = self._next_id()
        entry = {
            'id': entry_id,
            'text': text,
            'source': source,
            'created_at': datetime.now().isoformat()
        }
        
        data = self._load_data()
        data['entries'].append(entry)
        self._save_data(data)
        
        return entry_id
    
    def get_entry(self, entry_id: int) -> Optional[dict]:
        """Get an entry by ID.
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            Entry dict or None if not found
        """
        data = self._load_data()
        for entry in data['entries']:
            if entry['id'] == entry_id:
                return entry.copy()
        return None
    
    def update_entry(self, entry_id: int, text: Optional[str] = None, source: Optional[str] = None) -> bool:
        """Update an existing entry.
        
        Args:
            entry_id: ID of the entry to update
            text: New text (optional, if None keeps current)
            source: New source (optional, if None keeps current)
            
        Returns:
            True if updated, False if not found
            
        Raises:
            HolocronError: If text is provided but empty or whitespace-only
        """
        if text is not None and not text.strip():
            raise HolocronError("Text cannot be empty")
        
        data = self._load_data()
        for entry in data['entries']:
            if entry['id'] == entry_id:
                if text is not None:
                    entry['text'] = text
                if source is not None:
                    entry['source'] = source
                entry['updated_at'] = datetime.now().isoformat()
                self._save_data(data)
                return True
        return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID.
        
        Args:
            entry_id: ID of the entry to delete
            
        Returns:
            True if deleted, False if not found
        """
        data = self._load_data()
        original_count = len(data['entries'])
        data['entries'] = [e for e in data['entries'] if e['id'] != entry_id]
        
        if len(data['entries']) < original_count:
            self._save_data(data)
            return True
        return False
    
    def list_entries(self, limit: Optional[int] = None) -> list[dict]:
        """List all entries, newest first.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of entry dicts, ordered by created_at descending
        """
        data = self._load_data()
        entries = sorted(
            data['entries'],
            key=lambda e: e['created_at'],
            reverse=True
        )
        
        if limit is not None:
            entries = entries[:limit]
        
        return [e.copy() for e in entries]
    
    def search_entries(self, query: str) -> list[dict]:
        """Search entries by text (case-insensitive).
        
        Args:
            query: Search query
            
        Returns:
            List of matching entries
            
        Raises:
            HolocronError: If query is empty
        """
        if not query or not query.strip():
            raise HolocronError("Search query cannot be empty")
        
        query_lower = query.lower()
        data = self._load_data()
        
        results = [
            entry.copy()
            for entry in data['entries']
            if query_lower in entry['text'].lower()
        ]
        
        return sorted(results, key=lambda e: e['created_at'], reverse=True)
    
    def entry_count(self) -> int:
        """Get total number of entries."""
        data = self._load_data()
        return len(data['entries'])
