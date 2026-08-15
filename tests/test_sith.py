"""Tests for the sith (dark side) module."""

import pytest
from the_force.sith import (
    get_random_sith_quote,
    get_all_sith_quotes,
    sith_quote_count,
    get_sith_quote_by_index,
    format_sith_quote,
    get_sith_code,
    SITH_QUOTES,
)


class TestSithQuotes:
    """Test Sith quotes module."""

    def test_get_random_sith_quote_returns_string(self):
        """get_random_sith_quote should return a formatted string."""
        quote = get_random_sith_quote()
        assert isinstance(quote, str)
        assert len(quote) > 0
        assert " — " in quote

    def test_get_random_sith_quote_contains_known_quote(self):
        """get_random_sith_quote should return one of the known quotes."""
        quote = get_random_sith_quote()
        # Extract the quote part (before " — ")
        quote_text = quote.split(" — ")[0]
        known_texts = [entry['quote'] for entry in SITH_QUOTES]
        assert quote_text in known_texts

    def test_get_all_sith_quotes_returns_list(self):
        """get_all_sith_quotes should return a non-empty list."""
        quotes = get_all_sith_quotes()
        assert isinstance(quotes, list)
        assert len(quotes) > 0
        assert all(isinstance(q, str) for q in quotes)

    def test_sith_quote_count(self):
        """sith_quote_count should match the list length."""
        count = sith_quote_count()
        assert count == len(SITH_QUOTES)
        assert count > 0

    def test_get_sith_quote_by_index_valid(self):
        """get_sith_quote_by_index with valid index returns formatted quote."""
        quote = get_sith_quote_by_index(0)
        assert quote is not None
        expected = f"{SITH_QUOTES[0]['quote']} — {SITH_QUOTES[0]['author']}"
        assert quote == expected

    def test_get_sith_quote_by_index_negative(self):
        """get_sith_quote_by_index with negative index returns None."""
        quote = get_sith_quote_by_index(-1)
        assert quote is None

    def test_get_sith_quote_by_index_out_of_range(self):
        """get_sith_quote_by_index with out-of-range index returns None."""
        quote = get_sith_quote_by_index(9999)
        assert quote is None

    def test_format_sith_quote_default(self):
        """format_sith_quote should default to red color."""
        quote = "Test quote"
        formatted = format_sith_quote(quote)
        assert quote in formatted
        assert "\033[91m" in formatted  # Red

    def test_format_sith_quote_custom_color(self):
        """format_sith_quote should accept custom color."""
        quote = "Test"
        formatted = format_sith_quote(quote, color="purple")
        assert "\033[95m" in formatted  # Purple

    def test_get_sith_code_returns_string(self):
        """get_sith_code should return the Sith Code as a string."""
        code = get_sith_code()
        assert isinstance(code, str)
        assert len(code) > 0
        assert "peace" in code.lower()
        assert "power" in code.lower()

    def test_sith_quotes_have_required_fields(self):
        """All Sith quotes should have quote and author fields."""
        for entry in SITH_QUOTES:
            assert 'quote' in entry
            assert 'author' in entry
            assert isinstance(entry['quote'], str)
            assert isinstance(entry['author'], str)
            assert len(entry['quote']) > 0
            assert len(entry['author']) > 0
