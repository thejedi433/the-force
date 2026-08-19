"""Tests for the holocron module - personal wisdom journal."""

import pytest
import tempfile
import os
import json
from the_force.holocron import (
    Holocron,
    HolocronError,
)


class TestHolocron:
    """Test Holocron (wisdom journal) module."""

    def test_create_holocron_with_path(self, tmp_path):
        """Holocron should create storage at given path."""
        db_path = str(tmp_path / "test_holocron.json")
        holocron = Holocron(db_path)
        assert os.path.exists(db_path)
        # Should be valid JSON
        with open(db_path) as f:
            data = json.load(f)
        assert "entries" in data

    def test_add_entry_returns_id(self, tmp_path):
        """add_entry should return a positive integer ID."""
        holocron = Holocron(str(tmp_path / "h.json"))
        entry_id = holocron.add_entry("Test wisdom", source="Yoda")
        assert isinstance(entry_id, int)
        assert entry_id > 0

    def test_add_entry_empty_text_raises(self, tmp_path):
        """add_entry with empty text should raise HolocronError."""
        holocron = Holocron(str(tmp_path / "h.json"))
        with pytest.raises(HolocronError):
            holocron.add_entry("")

    def test_add_entry_whitespace_only_raises(self, tmp_path):
        """add_entry with whitespace-only text should raise HolocronError."""
        holocron = Holocron(str(tmp_path / "h.json"))
        with pytest.raises(HolocronError):
            holocron.add_entry("   \n\t  ")

    def test_get_entry_by_id(self, tmp_path):
        """get_entry should return the entry by ID."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Do or do not", source="Yoda")
        entry = holocron.get_entry(eid)
        assert entry is not None
        assert entry['id'] == eid
        assert entry['text'] == "Do or do not"
        assert entry['source'] == "Yoda"

    def test_get_entry_nonexistent_returns_none(self, tmp_path):
        """get_entry with unknown ID should return None."""
        holocron = Holocron(str(tmp_path / "h.json"))
        entry = holocron.get_entry(999)
        assert entry is None

    def test_delete_entry(self, tmp_path):
        """delete_entry should remove the entry."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Temporary wisdom")
        assert holocron.get_entry(eid) is not None
        result = holocron.delete_entry(eid)
        assert result is True
        assert holocron.get_entry(eid) is None

    def test_delete_nonexistent_returns_false(self, tmp_path):
        """delete_entry with unknown ID should return False."""
        holocron = Holocron(str(tmp_path / "h.json"))
        result = holocron.delete_entry(999)
        assert result is False

    def test_list_entries_empty(self, tmp_path):
        """list_entries on empty holocron returns empty list."""
        holocron = Holocron(str(tmp_path / "h.json"))
        entries = holocron.list_entries()
        assert entries == []

    def test_list_entries_order(self, tmp_path):
        """list_entries should return entries ordered by date (newest first)."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("First")
        holocron.add_entry("Second")
        holocron.add_entry("Third")
        entries = holocron.list_entries()
        assert len(entries) == 3
        assert entries[0]['text'] == "Third"
        assert entries[2]['text'] == "First"

    def test_search_entries(self, tmp_path):
        """search_entries should find matching entries."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("The Force is strong")
        holocron.add_entry("Use the Force")
        holocron.add_entry("I love tacos")
        results = holocron.search_entries("Force")
        assert len(results) == 2
        texts = [r['text'] for r in results]
        assert "The Force is strong" in texts
        assert "Use the Force" in texts
        assert "I love tacos" not in texts

    def test_search_entries_case_insensitive(self, tmp_path):
        """search_entries should be case-insensitive."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("THE FORCE AWAKENS")
        results = holocron.search_entries("force")
        assert len(results) == 1

    def test_search_entries_empty_query(self, tmp_path):
        """search_entries with empty query raises HolocronError."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("something")
        with pytest.raises(HolocronError):
            holocron.search_entries("")

    def test_entry_count(self, tmp_path):
        """entry_count should return number of stored entries."""
        holocron = Holocron(str(tmp_path / "h.json"))
        assert holocron.entry_count() == 0
        holocron.add_entry("One")
        assert holocron.entry_count() == 1
        holocron.add_entry("Two")
        assert holocron.entry_count() == 2

    def test_persistence_across_instances(self, tmp_path):
        """Entries should persist across Holocron instances."""
        path = str(tmp_path / "h.json")
        h1 = Holocron(path)
        h1.add_entry("Persistent wisdom", source="Yoda")
        
        h2 = Holocron(path)
        assert h2.entry_count() == 1
        entries = h2.list_entries()
        assert entries[0]['text'] == "Persistent wisdom"
        assert entries[0]['source'] == "Yoda"

    def test_entry_has_timestamp(self, tmp_path):
        """Each entry should have a created_at timestamp."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Timed wisdom")
        entry = holocron.get_entry(eid)
        assert 'created_at' in entry
        assert isinstance(entry['created_at'], str)
        assert len(entry['created_at']) > 0

    def test_add_entry_without_source(self, tmp_path):
        """add_entry with no source should store empty source."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Anonymous wisdom")
        entry = holocron.get_entry(eid)
        assert entry['source'] == ""

    def test_list_entries_with_limit(self, tmp_path):
        """list_entries with limit should return at most that many."""
        holocron = Holocron(str(tmp_path / "h.json"))
        for i in range(5):
            holocron.add_entry(f"Entry {i}")
        entries = holocron.list_entries(limit=3)
        assert len(entries) == 3

    def test_corrupted_file_handled(self, tmp_path):
        """Holocron should handle corrupted JSON files gracefully."""
        path = str(tmp_path / "h.json")
        with open(path, 'w') as f:
            f.write("this is not json!!!")
        holocron = Holocron(path)
        # Should reinitialize cleanly
        assert holocron.entry_count() == 0
        # Should be able to add entries
        eid = holocron.add_entry("Recovery wisdom")
        assert eid > 0

    def test_invalid_structure_handled(self, tmp_path):
        """Holocron should handle files with invalid structure."""
        path = str(tmp_path / "h.json")
        with open(path, 'w') as f:
            json.dump({"wrong_key": []}, f)
        holocron = Holocron(path)
        # Should reinitialize cleanly
        assert holocron.entry_count() == 0
        eid = holocron.add_entry("Fresh start")
        assert eid > 0

    def test_update_entry_text(self, tmp_path):
        """update_entry should change the text of an existing entry."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Original wisdom", source="Yoda")
        result = holocron.update_entry(eid, text="Updated wisdom")
        assert result is True
        entry = holocron.get_entry(eid)
        assert entry['text'] == "Updated wisdom"
        # Source should remain unchanged
        assert entry['source'] == "Yoda"

    def test_update_entry_source(self, tmp_path):
        """update_entry should change the source of an existing entry."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Some wisdom", source="Old Master")
        result = holocron.update_entry(eid, source="New Master")
        assert result is True
        entry = holocron.get_entry(eid)
        assert entry['source'] == "New Master"
        assert entry['text'] == "Some wisdom"

    def test_update_entry_both(self, tmp_path):
        """update_entry should change both text and source."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Old text", source="Old source")
        result = holocron.update_entry(eid, text="New text", source="New source")
        assert result is True
        entry = holocron.get_entry(eid)
        assert entry['text'] == "New text"
        assert entry['source'] == "New source"

    def test_update_entry_nonexistent_returns_false(self, tmp_path):
        """update_entry with unknown ID should return False."""
        holocron = Holocron(str(tmp_path / "h.json"))
        result = holocron.update_entry(999, text="anything")
        assert result is False

    def test_update_entry_empty_text_raises(self, tmp_path):
        """update_entry with empty text should raise HolocronError."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Original")
        with pytest.raises(HolocronError):
            holocron.update_entry(eid, text="")

    def test_update_entry_has_updated_at(self, tmp_path):
        """update_entry should add an updated_at timestamp."""
        import time
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Original")
        time.sleep(0.01)  # ensure different timestamp
        holocron.update_entry(eid, text="Modified")
        entry = holocron.get_entry(eid)
        assert 'updated_at' in entry
        assert entry['updated_at'] >= entry['created_at']

    def test_load_data_file_disappears(self, tmp_path):
        """_load_data should handle file disappearance during load."""
        path = str(tmp_path / "h.json")
        holocron = Holocron(path)
        # Add entry, then delete file
        holocron.add_entry("Test")
        os.remove(path)
        # Should return empty dict
        data = holocron._load_data()
        assert data == {"entries": []}

    def test_add_entry_with_tags(self, tmp_path):
        """add_entry should accept and store tags."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Wisdom about patience", tags=["patience", "jedi"])
        entry = holocron.get_entry(eid)
        assert 'tags' in entry
        assert isinstance(entry['tags'], list)
        assert "patience" in entry['tags']
        assert "jedi" in entry['tags']

    def test_add_entry_without_tags(self, tmp_path):
        """add_entry without tags should default to empty list."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Simple wisdom")
        entry = holocron.get_entry(eid)
        assert 'tags' in entry
        assert entry['tags'] == []

    def test_search_entries_by_tag(self, tmp_path):
        """search_entries should find entries by tag."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("Patience is key", tags=["patience"])
        holocron.add_entry("Strength in the Force", tags=["strength"])
        holocron.add_entry("Patient training", tags=["patience", "training"])
        results = holocron.search_entries(tag="patience")
        assert len(results) == 2
        texts = [r['text'] for r in results]
        assert "Patience is key" in texts
        assert "Patient training" in texts

    def test_search_entries_by_tag_case_insensitive(self, tmp_path):
        """search_entries by tag should be case-insensitive."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("Test", tags=["JEDI"])
        results = holocron.search_entries(tag="jedi")
        assert len(results) == 1

    def test_search_entries_combined_text_and_tag(self, tmp_path):
        """search_entries should support both text and tag filters."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("Force is strong", tags=["force"])
        holocron.add_entry("Dark side", tags=["dark"])
        holocron.add_entry("Force sensitivity", tags=["sensitivity"])
        results = holocron.search_entries(query="force", tag="force")
        assert len(results) == 1
        assert results[0]['text'] == "Force is strong"

    def test_update_entry_tags(self, tmp_path):
        """update_entry should allow updating tags."""
        holocron = Holocron(str(tmp_path / "h.json"))
        eid = holocron.add_entry("Wisdom", tags=["old"])
        result = holocron.update_entry(eid, tags=["new", "updated"])
        assert result is True
        entry = holocron.get_entry(eid)
        assert "new" in entry['tags']
        assert "updated" in entry['tags']
        assert "old" not in entry['tags']

    def test_get_all_tags(self, tmp_path):
        """get_all_tags should return list of all unique tags."""
        holocron = Holocron(str(tmp_path / "h.json"))
        holocron.add_entry("One", tags=["patience", "jedi"])
        holocron.add_entry("Two", tags=["strength"])
        holocron.add_entry("Three", tags=["patience", "wisdom"])
        tags = holocron.get_all_tags()
        assert isinstance(tags, list)
        assert "patience" in tags
        assert "jedi" in tags
        assert "strength" in tags
        assert "wisdom" in tags
        # Should be unique
        assert len(tags) == len(set(tags))

    def test_get_all_tags_empty(self, tmp_path):
        """get_all_tags on empty holocron returns empty list."""
        holocron = Holocron(str(tmp_path / "h.json"))
        tags = holocron.get_all_tags()
        assert tags == []
