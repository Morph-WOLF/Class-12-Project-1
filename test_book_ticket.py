import unittest
from unittest.mock import patch, MagicMock
import main

class TestBookTicket(unittest.TestCase):
    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_ac(self, mock_connect, mock_input, mock_searchtrain):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                (10101, 'Shatabdi Express', 'Delhi', 'Bhopal', 'monday,wednesday,friday', 'Running')
            ]
            mock_cursor.fetchone.return_value = (1500,)
            mock_input.side_effect = [
                '10101', '2', '1',           # train_no, tcktno, typ (AC)
                'Alice', '25', 'F',          # 1st ticket
                'Bob', '30', 'M'             # 2nd ticket
            ]
            main.Book_Ticket('testuser')
            self.assertTrue(mock_cursor.execute.call_count >= 3)
            self.assertTrue(mock_conn.commit.called)
        except Exception as e:
            self.fail(f"test_book_ticket_ac failed with error: {e}")

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_sl(self, mock_connect, mock_input, mock_searchtrain):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                (10101, 'Shatabdi Express', 'Delhi', 'Bhopal', 'monday,wednesday,friday', 'Running')
            ]
            mock_cursor.fetchone.return_value = (900,)
            mock_input.side_effect = [
                '10101', '1', '2',           # typ (SL)
                'Charlie', '40', 'M'
            ]
            main.Book_Ticket('testuser')
            self.assertTrue(mock_cursor.execute.call_count >= 2)
            self.assertTrue(mock_conn.commit.called)
        except Exception as e:
            self.fail(f"test_book_ticket_sl failed with error: {e}")

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_gen(self, mock_connect, mock_input, mock_searchtrain):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                (10101, 'Shatabdi Express', 'Delhi', 'Bhopal', 'monday,wednesday,friday', 'Running')
            ]
            mock_cursor.fetchone.return_value = (400,)
            mock_input.side_effect = [
                '10101', '1', '3',           # typ (GEN)
                'Daisy', '22', 'F'
            ]
            main.Book_Ticket('testuser')
            self.assertTrue(mock_cursor.execute.call_count >= 2)
            self.assertTrue(mock_conn.commit.called)
        except Exception as e:
            self.fail(f"test_book_ticket_gen failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
