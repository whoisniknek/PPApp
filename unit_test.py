import unittest
import _tkinter
from unittest.mock import patch, MagicMock
from main import (
    RegisterWindow, LoginWindow, ClientWindow, MasterWindow, ManagerWindow,
    AddRequestWindow, ChatWindow
)
from unittest.mock import ANY

class TestRegisterWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        mock_connect.return_value = self.mock_db_connection
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = RegisterWindow()
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_register_success(self):
        self.mock_cursor.fetchone.return_value = None
        self.app.login_entry.insert(0, "test_user")
        self.app.password_entry.insert(0, "test_password")
        self.app.fio_entry.insert(0, "Test User")
        self.app.phone_entry.insert(0, "1234567890")

        with patch('main.messagebox.showinfo') as mock_info:
            self.app.register()
            self.mock_cursor.execute.assert_any_call(
                ANY,
                ("Test User", "1234567890", "test_user", "test_password", "Заказчик")
            )
            mock_info.assert_called_with("Успех", "Регистрация успешна!")

class TestLoginWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        mock_connect.return_value = self.mock_db_connection
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = LoginWindow()
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_login_success(self):
        self.mock_cursor.fetchone.return_value = (1, "Клиент")
        self.app.login_entry.insert(0, "test_user")
        self.app.password_entry.insert(0, "test_password")

        with patch('main.ClientWindow') as mock_client_window:
            self.app.login()
            mock_client_window.assert_called_once()

class TestClientWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = ClientWindow("test_client", 1, self.mock_db_connection)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_load_requests(self):
        self.mock_cursor.fetchall.return_value = [(1, "2024-12-10", "Printer", "HP", "Doesn't work", "New")]
        self.app.load_requests()
        self.assertEqual(len(self.app.table.get_children()), 1)

class TestMasterWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = MasterWindow("test_master", 2, self.mock_db_connection)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_load_requests(self):
        self.mock_cursor.fetchall.return_value = [(2, "2024-12-10", "Laptop", "Dell", "Screen broken", "In progress")]
        self.app.load_requests()
        self.assertEqual(len(self.app.table.get_children()), 1)

class TestManagerWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = ManagerWindow("test_manager", 3, self.mock_db_connection)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_load_users(self):
        self.mock_cursor.fetchall.return_value = [(1, "Test User", "1234567890", "test_user", "Client")]
        self.app.load_users()
        self.assertEqual(len(self.app.users_table.get_children()), 1)

    def test_load_requests(self):
        self.mock_cursor.fetchall.return_value = [(3, "2024-12-10", "Monitor", "LG", "No display", "Completed", 1)]
        self.app.load_requests()
        self.assertEqual(len(self.app.requests_table.get_children()), 1)

class TestAddRequestWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        self.mock_update_callback = MagicMock()
        try:
            self.app = AddRequestWindow(1, self.mock_db_connection, self.mock_update_callback)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_add_request(self):
        self.app.device_type_input.insert(0, "Printer")
        self.app.model_input.insert(0, "Canon")
        self.app.problem_input.insert(0, "Paper jam")

        with patch('main.messagebox.showinfo') as mock_info:
            self.app.add_request()
            self.mock_cursor.execute.assert_any_call(
                ANY,
                ("Printer", "Canon", "Paper jam", 1)
            )
            mock_info.assert_called_with("Успех", "Заявка добавлена!")

class TestChatWindow(unittest.TestCase):
    @patch('main.pymysql.connect')
    def setUp(self, mock_connect):
        self.mock_db_connection = MagicMock()
        self.mock_cursor = self.mock_db_connection.cursor.return_value
        try:
            self.app = ChatWindow(1, 1, "Client", self.mock_db_connection)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.app = None

    def tearDown(self):
        if hasattr(self.app, 'tk') and self.app.tk is not None:
            try:
                self.app.destroy()
            except _tkinter.TclError as e:
                print(f"Window already destroyed: {e}")

    def test_load_messages(self):
        self.mock_cursor.fetchall.return_value = [("Test message", "Test User", "2024-12-10 10:00:00")]
        self.app.load_messages()
        self.assertEqual(self.app.messages_box.size(), 1)

if __name__ == "__main__":
    unittest.main()