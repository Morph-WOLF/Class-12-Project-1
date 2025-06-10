import unittest
from unittest.mock import patch, MagicMock
import main

class TestBookTicket(unittest.TestCase):
    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_ac(self, mock_connect, mock_input, mock_searchtrain):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Provide enough fetchall results for all calls
        mock_cursor.fetchall.side_effect = [
            [],  # fetchall after searchtrain
            [(1500,)],  # AC fare
        ]
        mock_input.side_effect = [
            'Delhi', 'Bhopal', 'monday',  # searchtrain inputs (not used due to patch)
            '10101', '2', '1',           # train_no, tcktno, typ (AC)
            'Alice', '25', 'F',          # 1st ticket
            'Bob', '30', 'M'             # 2nd ticket
        ]
        main.Book_Ticket('testuser')
        self.assertTrue(mock_cursor.execute.call_count >= 3)
        self.assertTrue(mock_conn.commit.called)

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_sl(self, mock_connect, mock_input, mock_searchtrain):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [],  # fetchall after searchtrain
            [(900,)],  # SL fare
        ]
        mock_input.side_effect = [
            'Delhi', 'Bhopal', 'monday',
            '10101', '1', '2',           # typ (SL)
            'Charlie', '40', 'M'
        ]
        main.Book_Ticket('testuser')
        self.assertTrue(mock_cursor.execute.call_count >= 2)
        self.assertTrue(mock_conn.commit.called)

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_gen(self, mock_connect, mock_input, mock_searchtrain):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [],  # fetchall after searchtrain
            [(400,)],  # GEN fare
        ]
        mock_input.side_effect = [
            'Delhi', 'Bhopal', 'monday',
            '10101', '1', '3',           # typ (GEN)
            'Daisy', '22', 'F'
        ]
        main.Book_Ticket('testuser')
        self.assertTrue(mock_cursor.execute.call_count >= 2)
        self.assertTrue(mock_conn.commit.called)

if __name__ == '__main__':
    unittest.main()
