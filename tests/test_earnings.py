"""
Tests for Earnings Calendar
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from src.earnings import EarningsCalendar

class TestEarningsCalendar(unittest.TestCase):
    def setUp(self):
        self.calendar = EarningsCalendar("fake_token")
    
    @patch('src.earnings.requests.get')
    def test_get_earnings_date_success(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'earningsCalendar': [
                {'date': '2026-03-15', 'epsActual': 2.5, 'epsEstimate': 2.3}
            ]
        }
        mock_get.return_value = mock_response
        
        date = self.calendar.get_earnings_date("AAPL")
        
        self.assertEqual(date, '2026-03-15')
        mock_get.assert_called_once()
    
    @patch('src.earnings.requests.get')
    def test_get_earnings_date_no_data(self, mock_get):
        # Mock empty response
        mock_response = Mock()
        mock_response.json.return_value = {'earningsCalendar': []}
        mock_get.return_value = mock_response
        
        date = self.calendar.get_earnings_date("AAPL")
        
        self.assertIsNone(date)
    
    @patch('src.earnings.requests.get')
    def test_get_earnings_date_api_error(self, mock_get):
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        date = self.calendar.get_earnings_date("AAPL")
        
        self.assertIsNone(date)
    
    @patch.object(EarningsCalendar, 'get_earnings_date')
    def test_is_safe_to_trade_no_earnings(self, mock_get_date):
        mock_get_date.return_value = None
        
        safe = self.calendar.is_safe_to_trade("AAPL", days_buffer=7)
        
        self.assertTrue(safe)
    
    @patch.object(EarningsCalendar, 'get_earnings_date')
    def test_is_safe_to_trade_far_earnings(self, mock_get_date):
        # Earnings 30 days away
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        mock_get_date.return_value = future_date
        
        safe = self.calendar.is_safe_to_trade("AAPL", days_buffer=7)
        
        self.assertTrue(safe)
    
    @patch.object(EarningsCalendar, 'get_earnings_date')
    def test_is_safe_to_trade_close_earnings(self, mock_get_date):
        # Earnings 3 days away
        future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        mock_get_date.return_value = future_date
        
        safe = self.calendar.is_safe_to_trade("AAPL", days_buffer=7)
        
        self.assertFalse(safe)
    
    @patch.object(EarningsCalendar, 'get_earnings_date')
    def test_is_safe_to_trade_past_earnings(self, mock_get_date):
        # Earnings already happened
        past_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        mock_get_date.return_value = past_date
        
        safe = self.calendar.is_safe_to_trade("AAPL", days_buffer=7)
        
        self.assertTrue(safe)

if __name__ == "__main__":
    unittest.main()
