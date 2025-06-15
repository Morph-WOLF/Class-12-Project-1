import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from your_module import TrainReservationSystem  # Replace with your actual module name

class TestTrainReservationSystem(unittest.TestCase):
    def setUp(self):
        # Setup for each test
        self.system = TrainReservationSystem()
        self.system.connector = MagicMock()
        self.system.current_user = None

    @patch('mysql.connector.connect')
    def test_db_connection(self, mock_connect):
        """Test database connection establishment"""
        mock_connect.return_value = MagicMock()
        system = TrainReservationSystem()
        self.assertIsNotNone(system.connector)

    def test_register_success(self):
        """Test successful user registration"""
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Simulate username not existing
        
        with patch('builtins.input', side_effect=['testuser', '1234567890', 'password']):
            result = self.system.register()
            self.assertEqual(result, 'testuser')
            mock_cursor.execute.assert_called()

    def test_register_existing_user(self):
        """Test registration with existing username"""
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)  # Simulate existing user
        
        with patch('builtins.input', side_effect=['existinguser', '1234567890', 'password']):
            result = self.system.register()
            self.assertIsNone(result)
            print("Registration with existing username correctly prevented")

    def test_login_success(self):
        """Test successful login"""
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'testuser', '1234567890', 'password')
        
        with patch('builtins.input', side_effect=['testuser', 'password']):
            result = self.system.login()
            self.assertEqual(result, 'testuser')
            self.assertEqual(self.system.current_user, 'testuser')
            print("Login successful with correct credentials")

    def test_login_failure(self):
        """Test failed login"""
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        with patch('builtins.input', side_effect=['wronguser', 'wrongpass']):
            result = self.system.login()
            self.assertIsNone(result)
            self.assertIsNone(self.system.current_user)
            print("Login correctly failed with wrong credentials")

    def test_search_train(self):
        """Test train search functionality"""
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (12345, 'Test Express', 'Station A', 'Station B', '08:00:00', '12:00:00', 100.0, 50.0, 25.0)
        ]
        
        with patch('builtins.input', side_effect=['Station A', 'Station B', 'monday']):
            result = self.system.search_train()
            self.assertEqual(len(result), 1)
            print("Train search returned correct results")

    def test_book_ticket_not_logged_in(self):
        """Test booking attempt without login"""
        self.system.current_user = None
        result = self.system.book_ticket()
        self.assertIsNone(result)
        print("Booking correctly prevented when not logged in")

    @patch.object(TrainReservationSystem, 'search_train')
    def test_book_ticket_success(self, mock_search):
        """Test successful ticket booking"""
        self.system.current_user = 'testuser'
        mock_search.return_value = [
            (12345, 'Test Express', 'Station A', 'Station B', '08:00:00', '12:00:00', 100.0, 50.0, 25.0)
        ]
        
        inputs = [
            '12345',    # Train number
            '1',        # AC class
            '2',        # 2 tickets
            'John Doe', # Passenger 1 name
            '30',       # Passenger 1 age
            'M',        # Passenger 1 gender
            'Jane Doe', # Passenger 2 name
            '28',       # Passenger 2 age
            'F',        # Passenger 2 gender
            'yes'       # Confirm booking
        ]
        
        with patch('builtins.input', side_effect=inputs):
            with patch('random.randint', return_value=999999):  # Mock PNR
                self.system.book_ticket()
                self.system.connector.commit.assert_called()
                print("Ticket booking completed successfully")

    def test_cancel_ticket_success(self):
        """Test successful ticket cancellation"""
        self.system.current_user = 'testuser'
        mock_cursor = MagicMock()
        self.system.connector.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'testuser', 999999, 12345, 'John Doe', 30, 'M', 100.0, 'AC', 'Confirmed')
        ]
        
        with patch('builtins.input', side_effect=['999999', 'yes']):
            self.system.cancel_ticket()
            self.system.connector.commit.assert_called()
            print("Ticket cancellation successful")

    def test_view_bookings_not_logged_in(self):
        """Test viewing bookings without login"""
        self.system.current_user = None
        result = self.system.view_bookings()
        self.assertIsNone(result)
        print("View bookings correctly prevented when not logged in")

    def tearDown(self):
        # Cleanup after each test
        if hasattr(self.system.connector, 'close'):
            self.system.connector.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)