from unittest import TestCase
from unittest.mock import Mock, patch
import requests

from backend.checker import status_code_checker, homeclimatcontrol_api_check

# unit test for get request
class TestStatusCodeChecker(TestCase):
    @patch("backend.checker.requests.get")
    def test_status_code_checker_returns_200(self, mock_get):
        fake_response = Mock()
        fake_response.status_code = 200

        mock_get.return_value = fake_response

        result = status_code_checker("https://example.com")

        self.assertEqual(result, 200)
    @patch("backend.checker.requests.get")
    def test_status_code_checker_returns_404(self, mock_get):
        fake_response = Mock()
        fake_response.status_code = 404
        mock_get.return_value = fake_response

        result = status_code_checker("https://example.com/notfound")

        self.assertEqual(result, 404)

    @patch("backend.checker.requests.get")
    def test_status_code_checker_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout("Connection timed out")

        with self.assertRaises(requests.Timeout):
            status_code_checker("https://example.com")

class TestHomeclimatcontrolApiCheck(TestCase):
    @patch("backend.checker.requests.get")
    def test_homeclimatcontrol_api_check(self, mock_get):
        fake_response = Mock()
        fake_response.json.return_value = {"success": True}
        
        mock_get.return_value = fake_response

        result = homeclimatcontrol_api_check("https://example.com")

        self.assertEqual(result, {"success": True})