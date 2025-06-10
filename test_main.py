import unittest
from unittest.mock import patch, MagicMock
import main

class TestTrainReservation(unittest.TestCase):
    @patch('builtins.input', side_effect=['testuser', '1234567890', 'testpass'])
    @patch('main.m.connect')
    def test_register_success(self, mock_connect, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        main.register()
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called_once()

    @patch('builtins.input', side_effect=['testuser', 'testpass'])
    @patch('main.m.connect')
    def test_login_success(self, mock_connect, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('sysid', 'testuser', '1234567890', 'testpass')

        result = main.login()
        self.assertEqual(result, 'testuser')

    @patch('builtins.input', side_effect=['wronguser', 'wrongpass'])
    @patch('main.m.connect')
    def test_login_failure(self, mock_connect, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = main.login()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()