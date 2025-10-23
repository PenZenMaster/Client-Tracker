"""Unit tests for logic module."""

import pytest
from unittest.mock import patch, MagicMock
from logic import run_background, run_gmb, run_faq, run_all


class TestLogicWorkflows:
    """Test suite for workflow orchestration functions."""

    @patch('logic.run_background_summary')
    def test_run_background_calls_summary_function(self, mock_run):
        """Test that run_background calls the background summary function."""
        config = {"name": "Test Business", "url": "https://example.com"}

        run_background(config)

        mock_run.assert_called_once_with(config)

    @patch('logic.run_gmb_keywords')
    def test_run_gmb_with_valid_services(self, mock_run):
        """Test GMB workflow with valid services list."""
        config = {
            "services": ["hvac repair", "ac installation", "heating maintenance"]
        }

        run_gmb(config)

        # Verify services were normalized (title case, stripped)
        assert config["services"] == ["Hvac Repair", "Ac Installation", "Heating Maintenance"]
        mock_run.assert_called_once_with(config)

    @patch('logic.run_gmb_keywords')
    def test_run_gmb_strips_whitespace_from_services(self, mock_run):
        """Test that GMB workflow strips whitespace from services."""
        config = {
            "services": ["  hvac repair  ", " ac installation", "heating maintenance  "]
        }

        run_gmb(config)

        assert config["services"] == ["Hvac Repair", "Ac Installation", "Heating Maintenance"]
        mock_run.assert_called_once()

    @patch('logic.run_gmb_keywords')
    def test_run_gmb_filters_empty_services(self, mock_run):
        """Test that GMB workflow filters out empty service strings."""
        config = {
            "services": ["hvac repair", "", "  ", "ac installation"]
        }

        run_gmb(config)

        # Empty and whitespace-only strings should be filtered out
        assert config["services"] == ["Hvac Repair", "Ac Installation"]
        mock_run.assert_called_once()

    def test_run_gmb_raises_error_when_no_services(self):
        """Test that run_gmb raises ValueError when no services provided."""
        config = {"services": []}

        with pytest.raises(ValueError, match="No services provided"):
            run_gmb(config)

    def test_run_gmb_raises_error_when_services_missing(self):
        """Test that run_gmb raises ValueError when services key missing."""
        config = {}

        with pytest.raises(ValueError, match="No services provided"):
            run_gmb(config)

    def test_run_gmb_raises_error_when_all_services_empty(self):
        """Test that run_gmb raises ValueError when all services are empty strings."""
        config = {"services": ["", "  ", "   "]}

        with pytest.raises(ValueError, match="No services provided"):
            run_gmb(config)

    @patch('logic.run_faq_generator')
    def test_run_faq_calls_generator_function(self, mock_run):
        """Test that run_faq calls the FAQ generator function."""
        config = {"seed_keyword": "HVAC contractor", "city": "NYC"}

        run_faq(config)

        mock_run.assert_called_once_with(config)

    @patch('logic.run_background_summary')
    @patch('logic.run_gmb_keywords')
    @patch('logic.run_faq_generator')
    def test_run_all_executes_all_workflows(self, mock_faq, mock_gmb, mock_bg):
        """Test that run_all executes all three workflows in sequence."""
        config = {
            "name": "Test Business",
            "services": ["hvac repair"],
            "seed_keyword": "HVAC"
        }

        run_all(config)

        # Verify all three functions were called
        mock_bg.assert_called_once_with(config)
        mock_gmb.assert_called_once_with(config)
        mock_faq.assert_called_once_with(config)

    @patch('logic.run_background_summary')
    @patch('logic.run_gmb_keywords')
    @patch('logic.run_faq_generator')
    def test_run_all_calls_in_correct_order(self, mock_faq, mock_gmb, mock_bg):
        """Test that run_all calls workflows in the correct order."""
        config = {
            "name": "Test Business",
            "services": ["service"],
            "seed_keyword": "keyword"
        }

        call_order = []
        mock_bg.side_effect = lambda c: call_order.append('background')
        mock_gmb.side_effect = lambda c: call_order.append('gmb')
        mock_faq.side_effect = lambda c: call_order.append('faq')

        run_all(config)

        assert call_order == ['background', 'gmb', 'faq']

    @patch('logic.run_background_summary')
    @patch('logic.run_gmb_keywords', side_effect=ValueError("Services error"))
    @patch('logic.run_faq_generator')
    def test_run_all_propagates_errors(self, mock_faq, mock_gmb, mock_bg):
        """Test that run_all propagates errors from individual workflows."""
        config = {"name": "Test", "services": [], "seed_keyword": "test"}

        with pytest.raises(ValueError, match="Services error"):
            run_all(config)

        # Background should have been called, but FAQ should not
        mock_bg.assert_called_once()
        mock_gmb.assert_called_once()
        mock_faq.assert_not_called()
