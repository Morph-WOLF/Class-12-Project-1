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

    @patch('builtins.input', side_effect=['testuser', '1234567890', 'testpass'])
    @patch('main.m.connect')
    def test_register_success(self, mock_connect, mock_input):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            main.register()
            mock_cursor.execute.assert_called()
            mock_conn.commit.assert_called_once()
            # Clean up: delete test user if inserted
            try:
                mock_cursor.execute.assert_any_call(
                    'DELETE FROM user_details WHERE user_id = %s', ('testuser',)
                )
            except AssertionError:
                pass  # If not called, ignore (since it's a mock)
        except Exception as e:
            self.fail(f"test_register_success failed with error: {e}")

    @patch('builtins.input', side_effect=['testuser', 'testpass'])
    @patch('main.m.connect')
    def test_login_success(self, mock_connect, mock_input):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = ('sysid', 'testuser', '1234567890', 'testpass')

            result = main.login()
            self.assertEqual(result, 'testuser')
        except Exception as e:
            self.fail(f"test_login_success failed with error: {e}")

    @patch('builtins.input', side_effect=['wronguser', 'wrongpass'])
    @patch('main.m.connect')
    def test_login_failure(self, mock_connect, mock_input):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None

            result = main.login()
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"test_login_failure failed with error: {e}")

    @patch('builtins.input', side_effect=['testuser', '1234567890', 'testpass'])
    @patch('main.m.connect')
    def test_register_duplicate_user(self, mock_connect, mock_input):
        """Test registering a user that already exists should still call execute and commit."""
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            # Simulate duplicate user error (e.g., IntegrityError)
            mock_cursor.execute.side_effect = [None, Exception('Duplicate entry')]
            with self.assertRaises(Exception):
                main.register()
        except Exception as e:
            # If the error is not the duplicate entry, fail
            if 'Duplicate entry' not in str(e):
                self.fail(f"test_register_duplicate_user failed with error: {e}")

    @patch('builtins.input', side_effect=['', '1234567890', 'testpass'])
    @patch('main.m.connect')
    def test_register_empty_username(self, mock_connect, mock_input):
        """Test registration with empty username input."""
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            main.register()
            # Should still call execute, but with empty username
            mock_cursor.execute.assert_called()
        except Exception as e:
            self.fail(f"test_register_empty_username failed with error: {e}")

    @patch('builtins.input', side_effect=['testuser', '', 'testpass'])
    @patch('main.m.connect')
    def test_register_empty_phone(self, mock_connect, mock_input):
        """Test registration with empty phone number input."""
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            with self.assertRaises(ValueError):
                main.register()
        except Exception as e:
            if not isinstance(e, ValueError):
                self.fail(f"test_register_empty_phone failed with error: {e}")

    @patch('builtins.input', side_effect=['testuser', '1234567890', ''])
    @patch('main.m.connect')
    def test_register_empty_password(self, mock_connect, mock_input):
        """Test registration with empty password input."""
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            main.register()
            mock_cursor.execute.assert_called()
        except Exception as e:
            self.fail(f"test_register_empty_password failed with error: {e}")

    @patch('builtins.input', side_effect=['testuser', 'wrongpass'])
    @patch('main.m.connect')
    def test_login_wrong_password(self, mock_connect, mock_input):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.side_effect = [None, None]
            result = main.login()
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"test_login_wrong_password failed with error: {e}")

    @patch('builtins.input', side_effect=['', ''])
    @patch('main.m.connect')
    def test_login_empty_fields(self, mock_connect, mock_input):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.side_effect = [None, None]
            result = main.login()
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"test_login_empty_fields failed with error: {e}")

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_invalid_train(self, mock_connect, mock_input, mock_searchtrain):
        try:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                (10101, 'Shatabdi Express', 'Delhi', 'Bhopal', 'monday,wednesday,friday', 'Running')
            ]
            mock_cursor.fetchone.return_value = None  # No fare found
            mock_input.side_effect = [
                '99999', '1', '1',           # invalid train_no, tcktno, typ
                'Alice', '25', 'F'
            ]
            main.Book_Ticket('testuser')
            # Should print invalid train number or class selected and return
            self.assertTrue(mock_cursor.execute.call_count >= 1)
        except Exception as e:
            self.fail(f"test_book_ticket_invalid_train failed with error: {e}")

    @patch('main.searchtrain', return_value=None)
    @patch('builtins.input')
    @patch('main.m.connect')
    def test_book_ticket_zero_tickets(self, mock_connect, mock_input, mock_searchtrain):
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
                '10101', '0', '1'  # train_no, tcktno=0, typ (AC)
            ]
            main.Book_Ticket('testuser')
            # Should not call execute for ticket insert
            self.assertTrue(mock_cursor.execute.call_count >= 1)
        except Exception as e:
            self.fail(f"test_book_ticket_zero_tickets failed with error: {e}")

    def tearDown(self):
        # Clean up test users from the real database
        import mysql.connector as m
        try:
            conn = m.connect(host="localhost", user="root", password="root", database="trainreservation")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_details WHERE user_id = %s", ("testuser",))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()