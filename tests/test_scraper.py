"""Unit tests for scraper module."""

import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException, Timeout, ConnectionError
from scraper import scrape_website_text


class TestScraperWebsiteText:
    """Test suite for scrape_website_text function."""

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_successful_scrape_returns_text(self, mock_soup, mock_get):
        """Test successful website scraping returns extracted text."""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '<html><body><h1>Title</h1><p>Content</p></body></html>'
        mock_get.return_value = mock_response

        # Mock BeautifulSoup
        mock_tag1 = MagicMock()
        mock_tag1.get_text.return_value = 'Title'
        mock_tag2 = MagicMock()
        mock_tag2.get_text.return_value = 'Content'

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = [mock_tag1, mock_tag2]
        mock_soup.return_value = mock_soup_instance

        result = scrape_website_text('https://example.com')

        assert result == 'Title\nContent'
        mock_get.assert_called_once_with('https://example.com', timeout=10)

    @patch('scraper.requests.get')
    def test_request_timeout_returns_empty_string(self, mock_get):
        """Test that request timeout returns empty string."""
        mock_get.side_effect = Timeout("Connection timeout")

        result = scrape_website_text('https://example.com')

        assert result == ''

    @patch('scraper.requests.get')
    def test_connection_error_returns_empty_string(self, mock_get):
        """Test that connection error returns empty string."""
        mock_get.side_effect = ConnectionError("Connection failed")

        result = scrape_website_text('https://example.com')

        assert result == ''

    @patch('scraper.requests.get')
    def test_general_request_exception_returns_empty_string(self, mock_get):
        """Test that general RequestException returns empty string."""
        mock_get.side_effect = RequestException("Request failed")

        result = scrape_website_text('https://example.com')

        assert result == ''

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_respects_max_paragraphs_limit(self, mock_soup, mock_get):
        """Test that scraper respects max_paragraphs parameter."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        # Create 10 mock tags
        mock_tags = []
        for i in range(10):
            tag = MagicMock()
            tag.get_text.return_value = f'Paragraph {i}'
            mock_tags.append(tag)

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = mock_tags
        mock_soup.return_value = mock_soup_instance

        result = scrape_website_text('https://example.com', max_paragraphs=5)

        # Should only return first 5 paragraphs
        lines = result.split('\n')
        assert len(lines) == 5
        assert lines[0] == 'Paragraph 0'
        assert lines[4] == 'Paragraph 4'

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_removes_script_and_style_elements(self, mock_soup, mock_get):
        """Test that script and style elements are removed."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_elements = [MagicMock() for _ in range(6)]  # script, style, header, footer, nav, form
        mock_soup_instance.return_value = mock_elements
        mock_soup_instance.find_all.return_value = []
        mock_soup.return_value = mock_soup_instance

        scrape_website_text('https://example.com')

        # Verify decompose was called on unwanted elements
        mock_soup_instance.assert_called_with(['script', 'style', 'header', 'footer', 'nav', 'form'])

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_filters_empty_text_blocks(self, mock_soup, mock_get):
        """Test that empty text blocks are filtered out."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        # Create tags with some empty text
        mock_tag1 = MagicMock()
        mock_tag1.get_text.return_value = 'Valid text'
        mock_tag2 = MagicMock()
        mock_tag2.get_text.return_value = ''
        mock_tag3 = MagicMock()
        mock_tag3.get_text.return_value = 'Another valid text'

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = [mock_tag1, mock_tag2, mock_tag3]
        mock_soup.return_value = mock_soup_instance

        result = scrape_website_text('https://example.com')

        # Empty text block should be filtered
        assert result == 'Valid text\nAnother valid text'

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_searches_for_h1_h2_p_tags(self, mock_soup, mock_get):
        """Test that scraper searches for h1, h2, and p tags."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = []
        mock_soup.return_value = mock_soup_instance

        scrape_website_text('https://example.com')

        # Verify find_all was called with correct tag list
        mock_soup_instance.find_all.assert_called_with(['h1', 'h2', 'p'])

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_uses_lxml_parser(self, mock_soup, mock_get):
        """Test that BeautifulSoup uses lxml parser."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = []
        mock_soup.return_value = mock_soup_instance

        scrape_website_text('https://example.com')

        # Verify BeautifulSoup was called with lxml parser
        mock_soup.assert_called_once()
        args = mock_soup.call_args
        assert args[0][1] == 'lxml'

    @patch('scraper.requests.get')
    @patch('scraper.BeautifulSoup')
    def test_strips_whitespace_from_text(self, mock_soup, mock_get):
        """Test that text is stripped of whitespace."""
        mock_response = MagicMock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response

        mock_tag = MagicMock()
        mock_tag.get_text.return_value = '  Spaced text  '

        mock_soup_instance = MagicMock()
        mock_soup_instance.find_all.return_value = [mock_tag]
        mock_soup.return_value = mock_soup_instance

        scrape_website_text('https://example.com')

        # Verify get_text was called with strip=True
        mock_tag.get_text.assert_called_with(strip=True)
