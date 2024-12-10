import tkinter as tk
from tkinter import messagebox,ttk
import pymysql

class RegisterWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Регистрация")
        self.geometry("400x500")  # Увеличим высоту окна

        # Поля для ввода логина, пароля, роли, ФИО и телефона
        tk.Label(self, text="Логин").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack(pady=5)

        tk.Label(self, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self, text="Роль").pack(pady=5)
        # Список ролей для выбора
        roles = ['Заказчик']
        self.role_var = tk.StringVar(self)
        self.role_var.set(roles[0])  # Устанавливаем дефолтную роль
        self.role_menu = tk.OptionMenu(self, self.role_var, *roles)
        self.role_menu.pack(pady=5)

        tk.Label(self, text="ФИО").pack(pady=5)
        self.fio_entry = tk.Entry(self)
        self.fio_entry.pack(pady=5)

        tk.Label(self, text="Телефон").pack(pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack(pady=5)

        # Размещение кнопок в одну линию
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Кнопка для регистрации
        self.register_button = tk.Button(button_frame, text="Зарегистрироваться", command=self.register)
        self.register_button.pack(side="left",pady= 10)

        # Кнопка для перехода к окну входа
        self.login_button = tk.Button(button_frame, text="Уже зарегистрированы? Войти", command=self.go_to_login)
        self.login_button.pack(side="left", pady= 10)

        # Подключение к базе данных через pymysql
        try:
            self.db_connection = pymysql.connect(
                host="localhost",       # Адрес сервера MySQL
                user="root",            # Имя пользователя
                password="root",        # Пароль пользователя
                database="niknekpp"          # Имя базы данных
            )
            self.db_cursor = self.db_connection.cursor()
            print("Соединение с базой данных успешно установлено!")
        except pymysql.MySQLError as err:
            messagebox.showerror("Ошибка подключения", f"Ошибка подключения к базе данных: {err}")
            self.quit()

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()  # Получаем выбранную роль
        fio = self.fio_entry.get()
        phone = self.phone_entry.get()

        if not login or not password or not role or not fio or not phone:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверка, существует ли уже такой логин
        query = "SELECT * FROM User WHERE login = %s"
        self.db_cursor.execute(query, (login,))
        if self.db_cursor.fetchone():
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
            return

        # Регистрация нового пользователя
        query = """
            INSERT INTO User (fio, phone, login, password, type) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.db_cursor.execute(query, (fio, phone, login, password, role))
        self.db_connection.commit()

        messagebox.showinfo("Успех", "Регистрация успешна!")
        self.destroy()
        app = LoginWindow()  # Переход в окно входа
        app.mainloop()

    def go_to_login(self):
        self.destroy()
        app = LoginWindow()  # Переход в окно входа
        app.mainloop()

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Вход в систему")
        self.geometry("400x300")

        # Поля для ввода логина и пароля
        tk.Label(self, text="Логин").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack(pady=5)

        tk.Label(self, text="Пароль").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Размещение кнопок в одну линию
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Кнопка для входа
        self.login_button = tk.Button(button_frame, text="Войти", command=self.login)
        self.login_button.pack(side="left", pady= 10)

        # Кнопка для перехода к окну регистрации
        self.register_button = tk.Button(button_frame, text="Зарегистрироваться", command=self.go_to_register)
        self.register_button.pack(side="left", padx=5)

        # Подключение к базе данных через pymysql
        try:
            self.db_connection = pymysql.connect(
                host="localhost",       # Адрес сервера MySQL
                user="root",            # Имя пользователя
                password="root",        # Пароль пользователя
                database="niknekpp"          # Имя базы данных
            )
            self.db_cursor = self.db_connection.cursor()
            print("Соединение с базой данных успешно установлено!")
        except pymysql.MySQLError as err:
            messagebox.showerror("Ошибка подключения", f"Ошибка подключения к базе данных: {err}")
            self.quit()

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите логин и пароль.")
            return

        # Проверка данных в базе
        query = "SELECT userID, type FROM User WHERE login = %s AND password = %s"
        self.db_cursor.execute(query, (login, password))
        result = self.db_cursor.fetchone()

        if result:
            user_id, user_type = result
            self.destroy()  # Закрываем окно входа
            if user_type == 'Клиент':
                app = ClientWindow(login, user_id, self.db_connection)
                app.mainloop()
            elif user_type == 'Мастер':
                app = MasterWindow(login, user_id, self.db_connection)
                app.mainloop()
            elif user_type == 'Администратор':
                app = ManagerWindow(login, user_id, self.db_connection)  # Теперь добавлен ManagerWindow
                app.mainloop()
            else:
                messagebox.showinfo("Ошибка", f"Роль {user_type} еще не поддерживается!")
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def go_to_register(self):
        self.destroy()
        app = RegisterWindow()  # Переход в окно регистрации
        app.mainloop()


class ClientWindow(tk.Tk):
    def __init__(self, client_login, client_id, db_connection):
        super().__init__()

        self.client_login = client_login
        self.client_id = client_id
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

        self.title(f"Заявки клиента: {client_login}")
        self.geometry("800x600")

        # Таблица заявок клиента
        self.create_table()

        # Кнопка для добавления заявки
        add_button = tk.Button(self, text="Добавить новую заявку", command=self.add_request)
        add_button.pack(pady=10)
        chat_button = tk.Button(self, text="Открыть чат", command=self.open_chat)
        chat_button.pack(pady=10)

        # Загружаем заявки клиента
        self.load_requests()

    def open_chat(self):
    # Получаем ID выбранной заявки
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для открытия чата.")
            return

        request_id = self.table.item(selected_item)["values"][0]
        app = ChatWindow(request_id, self.client_id, "Клиент", self.db_connection)
        app.mainloop()

    def create_table(self):
        # Таблица заявок
        self.table = ttk.Treeview(self, columns=("number", "date", "device_type", "model", "problem", "status"), show="headings")
        self.table.heading("number", text="Номер")
        self.table.heading("date", text="Дата")
        self.table.heading("device_type", text="Вид оргтехники")
        self.table.heading("model", text="Модель")
        self.table.heading("problem", text="Описание проблемы")
        self.table.heading("status", text="Статус")

        self.table.column("number", width=50)
        self.table.column("date", width=100)
        self.table.column("device_type", width=100)
        self.table.column("model", width=100)
        self.table.column("problem", width=150)
        self.table.column("status", width=100)

        self.table.pack(fill=tk.BOTH, expand=True)

    def load_requests(self):
        query = """
        SELECT r.requestID, r.startDate, r.orgTechType, r.orgTechModel, r.problemDescription, r.requestStatus
        FROM Request r
        WHERE r.clientID = %s
        """
        self.db_cursor.execute(query, (self.client_id,))
        requests = self.db_cursor.fetchall()

        for request in requests:
            if request[-1] != "Новая заявка":  # Если статус изменился
                messagebox.showinfo("Уведомление", f"Статус заявки {request[0]}: {request[-1]}")
            self.table.insert("", "end", values=request)

    def add_request(self):
        # Открытие окна для добавления новой заявки
        AddRequestWindow(self.client_id, self.db_connection, self.load_requests)


class MasterWindow(tk.Tk):
    def __init__(self, master_login, master_id, db_connection):
        super().__init__()

        self.master_login = master_login
        self.master_id = master_id
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

        self.title(f"Заявки мастера: {master_login}")
        self.geometry("800x600")

        # Таблица заявок мастера
        self.create_table()

        # Кнопка для изменения статуса заявки
        change_status_button = tk.Button(self, text="Изменить статус заявки", command=self.change_status)
        change_status_button.pack(pady=10)

        # Кнопка для добавления комментария
        add_comment_button = tk.Button(self, text="Добавить комментарий", command=self.add_comment)
        add_comment_button.pack(pady=10)

        accept_new_requests_button = tk.Button(self, text="Показать новые заявки", command=self.open_new_requests)
        accept_new_requests_button.pack(pady=10)
        chat_button = tk.Button(self, text="Открыть чат", command=self.open_chat)
        chat_button.pack(pady=10)
        # Загружаем заявки мастера
        self.load_requests()


    def open_chat(self):
        # Получаем ID выбранной заявки
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для открытия чата.")
            return

        request_id = self.table.item(selected_item)["values"][0]
        app = ChatWindow(request_id, self.master_id, "Мастер", self.db_connection)
        app.mainloop()
    def open_new_requests(self):
        # Окно для отображения заявок с статусом "Новая заявка"
        new_requests_window = tk.Toplevel(self)
        new_requests_window.title("Новые заявки")
        new_requests_window.geometry("800x600")

        # Таблица для отображения заявок
        new_requests_table = ttk.Treeview(new_requests_window,
                                          columns=("number", "date", "device_type", "model", "problem", "status"),
                                          show="headings")
        new_requests_table.heading("number", text="Номер")
        new_requests_table.heading("date", text="Дата")
        new_requests_table.heading("device_type", text="Вид оргтехники")
        new_requests_table.heading("model", text="Модель")
        new_requests_table.heading("problem", text="Описание проблемы")
        new_requests_table.heading("status", text="Статус")

        new_requests_table.column("number", width=50)
        new_requests_table.column("date", width=100)
        new_requests_table.column("device_type", width=100)
        new_requests_table.column("model", width=100)
        new_requests_table.column("problem", width=150)
        new_requests_table.column("status", width=100)

        new_requests_table.pack(fill=tk.BOTH, expand=True)

        # Загрузка заявок с статусом "Новая заявка"
        query = """
        SELECT r.requestID, r.startDate, r.orgTechType, r.orgTechModel, r.problemDescription, r.requestStatus
        FROM Request r
        WHERE r.requestStatus = 'Новая заявка'
        """
        self.db_cursor.execute(query)
        new_requests = self.db_cursor.fetchall()

        for request in new_requests:
            new_requests_table.insert("", "end", values=request)

        def accept_selected_request():
            selected_item = new_requests_table.selection()
            if not selected_item:
                messagebox.showwarning("Ошибка", "Выберите заявку для принятия.")
                return

            request_id = new_requests_table.item(selected_item)["values"][0]
            query = "UPDATE Request SET requestStatus = 'В процессе ремонта', masterID = %s WHERE requestID = %s"
            self.db_cursor.execute(query, (self.master_id, request_id))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Заявка принята!")
            new_requests_window.destroy()  # Закрываем окно
            self.load_requests()  # Обновляем заявки

        accept_button = tk.Button(new_requests_window, text="Принять заявку", command=accept_selected_request)
        accept_button.pack(pady=10)

    def create_table(self):
        # Таблица заявок
        self.table = ttk.Treeview(self, columns=("number", "date", "device_type", "model", "problem", "status"), show="headings")
        self.table.heading("number", text="Номер")
        self.table.heading("date", text="Дата")
        self.table.heading("device_type", text="Вид оргтехники")
        self.table.heading("model", text="Модель")
        self.table.heading("problem", text="Описание проблемы")
        self.table.heading("status", text="Статус")

        self.table.column("number", width=50)
        self.table.column("date", width=100)
        self.table.column("device_type", width=100)
        self.table.column("model", width=100)
        self.table.column("problem", width=150)
        self.table.column("status", width=100)

        self.table.pack(fill=tk.BOTH, expand=True)

    def load_requests(self):
        # Очищаем таблицу перед загрузкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Загрузка заявок, назначенных данному мастеру через userID
        query = """
        SELECT requestID, startDate, orgTechType, orgTechModel, problemDescription, requestStatus
        FROM Request r
        WHERE masterid = %s
        """
        self.db_cursor.execute(query, (self.master_id,))
        requests = self.db_cursor.fetchall()

        for request in requests:
            self.table.insert("", "end", values=request)

    def change_status(self):
        # Выбор заявки для изменения статуса
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для изменения статуса.")
            return

        request_id = self.table.item(selected_item)["values"][0]
        self.update_status(request_id)

    def update_status(self, request_id):
        # Окно для выбора нового статуса
        status_options = ['Новая заявка', 'В процессе ремонта', 'Готова к выдаче']
        status_window = tk.Toplevel(self)
        status_window.title("Выберите статус")
        status_window.geometry("300x150")

        selected_status = tk.StringVar(status_window)
        selected_status.set(status_options[0])

        status_menu = ttk.Combobox(status_window, textvariable=selected_status, values=status_options)
        status_menu.pack(pady=20)

        def confirm():
            new_status = selected_status.get()
            # Обновление статуса заявки в базе данных
            query = """
            UPDATE Request
            SET requestStatus = %s
            WHERE requestID = %s
            """
            self.db_cursor.execute(query, (new_status, request_id))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Статус заявки изменен!")
            self.load_requests()  # Обновляем таблицу заявок
            status_window.destroy()

        confirm_button = tk.Button(status_window, text="Подтвердить", command=confirm)
        confirm_button.pack(pady=10)

    def add_comment(self):
        # Выбор заявки для добавления комментария
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для добавления комментария.")
            return

        request_id = self.table.item(selected_item)["values"][0]
        self.open_comment_window(request_id)

    def open_comment_window(self, request_id):
        # Окно для добавления комментария
        comment_window = tk.Toplevel(self)
        comment_window.title("Добавить комментарий")
        comment_window.geometry("400x300")

        tk.Label(comment_window, text="Введите комментарий").pack(pady=10)
        comment_text = tk.Text(comment_window, width=50, height=10)
        comment_text.pack(pady=10)

        def save_comment():
            message = comment_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showerror("Ошибка", "Комментарий не может быть пустым.")
                return

            # Вставка комментария в базу данных
            query = """
            INSERT INTO Comment (message, masterID, requestID)
            VALUES (%s, %s, %s)
            """
            self.db_cursor.execute(query, (message, self.master_id, request_id))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Комментарий добавлен!")
            comment_window.destroy()

        save_button = tk.Button(comment_window, text="Сохранить", command=save_comment)
        save_button.pack(pady=10)

class ChatWindow(tk.Toplevel):
    def __init__(self, request_id, user_id, user_type, db_connection):
        super().__init__()

        self.request_id = request_id
        self.user_id = user_id
        self.user_type = user_type
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

        self.title("Чат")
        self.geometry("400x400")

        # Заголовок
        self.chat_title = tk.Label(self, text="Чат", font=("Arial", 16))
        self.chat_title.pack(pady=10)

        # Поле для отображения сообщений
        self.messages_box = tk.Listbox(self, height=15, width=100, selectmode=tk.SINGLE)
        self.messages_box.pack(pady=10)

        # Поле для ввода нового сообщения
        self.message_input = tk.Entry(self, width=40)
        self.message_input.pack(pady=5)

        # Кнопка отправки сообщения
        self.send_button = tk.Button(self, text="Отправить", command=self.send_message)
        self.send_button.pack(pady=5)

        # Загрузка существующих сообщений
        self.load_messages()

        # Обновление сообщений
        self.after(2000, self.load_messages)  # Обновление чата каждые 2 секунды

    def load_messages(self):
        # Очистка поля сообщений
        self.messages_box.delete(0, tk.END)

        # Загрузка комментариев из базы данных
        query = """
        SELECT c.message, u.fio, c.timestamp
        FROM Comment c
        JOIN User u ON c.masterID = u.userID
        WHERE c.requestID = %s
        ORDER BY c.timestamp
        """
        self.db_cursor.execute(query, (self.request_id,))
        messages = self.db_cursor.fetchall()

        # Отображение сообщений в чате
        for message in messages:
            message_text = f"{message[1]} ({message[2]}): {message[0]}"
            self.messages_box.insert(tk.END, message_text)

    def send_message(self):
        # Получаем текст нового сообщения
        message_text = self.message_input.get()

        if not message_text:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите сообщение.")
            return

        # Добавление сообщения в базу данных
        query = """
        INSERT INTO Comment (message, masterID, requestID)
        VALUES (%s, %s, %s)
        """
        self.db_cursor.execute(query, (message_text, self.user_id, self.request_id))
        self.db_connection.commit()

        self.message_input.delete(0, tk.END)  # Очистка поля ввода
        self.load_messages()  # Обновление чата


class ManagerWindow(tk.Tk):
    def __init__(self, manager_login, manager_id, db_connection):
        super().__init__()

        self.manager_login = manager_login
        self.manager_id = manager_id
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()

        self.title(f"Менеджер: {manager_login}")
        self.geometry("600x600")  # Уменьшенный размер окна

        # Создаем вкладки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создаем вкладки для заявок и пользователей
        self.create_users_tab()
        self.create_requests_tab()


        # Фрейм для кнопок
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10)

        # Кнопки для управления заявками
        self.delete_request_button = tk.Button(buttons_frame, text="Удалить заявку", command=self.delete_request)
        self.delete_request_button.pack(side=tk.LEFT, padx=5)

        self.change_status_button = tk.Button(buttons_frame, text="Изменить статус заявки", command=self.change_status)
        self.change_status_button.pack(side=tk.LEFT, padx=5)


        # Кнопки для управления пользователями
        self.delete_user_button = tk.Button(buttons_frame, text="Удалить пользователя", command=self.delete_user)
        self.delete_user_button.pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(self.requests_tab)
        self.search_entry.pack(pady=5)
        search_button = tk.Button(self.requests_tab, text="Найти заявку", command=self.search_request)
        search_button.pack(pady=5)

        # Загружаем все заявки и пользователей
        self.load_requests()
        self.load_users()

    def search_request(self):
        search_term = self.search_entry.get()
        query = """
        SELECT requestID, startDate, orgTechType, orgTechModel, problemDescription, requestStatus, clientID
        FROM Request
        WHERE requestID = %s OR orgTechType LIKE %s
        """
        self.db_cursor.execute(query, (search_term, f"%{search_term}%"))
        results = self.db_cursor.fetchall()

        for row in self.requests_table.get_children():
            self.requests_table.delete(row)

        for result in results:
            self.requests_table.insert("", "end", values=result)

    def create_requests_tab(self):
        # Вкладка для таблицы заявок
        self.requests_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.requests_tab, text="Заявки")

        # Таблица заявок
        self.requests_table = ttk.Treeview(self.requests_tab, columns=("number", "date", "device_type", "model", "problem", "status", "client_id"), show="headings")
        self.requests_table.heading("number", text="Номер")
        self.requests_table.heading("date", text="Дата")
        self.requests_table.heading("device_type", text="Вид оргтехники")
        self.requests_table.heading("model", text="Модель")
        self.requests_table.heading("problem", text="Описание проблемы")
        self.requests_table.heading("status", text="Статус")
        self.requests_table.heading("client_id", text="ID клиента")

        self.requests_table.column("number", width=50)
        self.requests_table.column("date", width=100)
        self.requests_table.column("device_type", width=100)
        self.requests_table.column("model", width=100)
        self.requests_table.column("problem", width=150)
        self.requests_table.column("status", width=100)
        self.requests_table.column("client_id", width=100)

        self.requests_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_users_tab(self):
        # Вкладка для таблицы пользователей
        self.users_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.users_tab, text="Пользователи")

        # Таблица пользователей
        self.users_table = ttk.Treeview(self.users_tab, columns=("user_id", "fio", "phone", "login", "role"), show="headings")
        self.users_table.heading("user_id", text="ID")
        self.users_table.heading("fio", text="ФИО")
        self.users_table.heading("phone", text="Телефон")
        self.users_table.heading("login", text="Логин")
        self.users_table.heading("role", text="Роль")

        self.users_table.column("user_id", width=50)
        self.users_table.column("fio", width=150)
        self.users_table.column("phone", width=100)
        self.users_table.column("login", width=100)
        self.users_table.column("role", width=100)

        self.users_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_requests(self):
        # Очищаем таблицу перед загрузкой новых данных
        for row in self.requests_table.get_children():
            self.requests_table.delete(row)

        # Загрузка всех заявок из базы данных
        query = """
        SELECT r.requestID, r.startDate, r.orgTechType, r.orgTechModel, r.problemDescription, r.requestStatus, r.clientID
        FROM Request r
        """
        self.db_cursor.execute(query)
        requests = self.db_cursor.fetchall()

        for request in requests:
            self.requests_table.insert("", "end", values=request)

    def load_users(self):
        # Очищаем таблицу пользователей
        for row in self.users_table.get_children():
            self.users_table.delete(row)

        # Загрузка всех пользователей из базы данных
        query = """
        SELECT userid, fio, phone, login, type
        FROM User
        """
        self.db_cursor.execute(query)
        users = self.db_cursor.fetchall()

        for user in users:
            self.users_table.insert("", "end", values=user)

    def delete_request(self):
        # Выбор заявки для удаления
        selected_item = self.requests_table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для удаления.")
            return

        request_id = self.requests_table.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить эту заявку?")
        if confirm:
            # Удаление заявки из базы данных
            query = "DELETE FROM Request WHERE requestID = %s"
            self.db_cursor.execute(query, (request_id,))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Заявка удалена!")
            self.load_requests()  # Обновляем таблицу заявок

    def delete_user(self):
        # Выбор пользователя для удаления
        selected_item = self.users_table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите пользователя для удаления.")
            return

        user_id = self.users_table.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить этого пользователя?")
        if confirm:
            # Удаление пользователя из базы данных
            query = "DELETE FROM User WHERE userID = %s"
            self.db_cursor.execute(query, (user_id,))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Пользователь удален!")
            self.load_users()  # Обновляем таблицу пользователей

    def change_status(self):
        # Выбор заявки для изменения статуса
        selected_item = self.requests_table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для изменения статуса.")
            return

        request_id = self.requests_table.item(selected_item)["values"][0]
        self.update_status(request_id)

    def update_status(self, request_id):
        # Окно для выбора нового статуса
        status_options = ['Новая заявка', 'В процессе ремонта', 'Готова к выдаче', 'Завершена']
        status_window = tk.Toplevel(self)
        status_window.title("Выберите статус")
        status_window.geometry("250x150")  # Уменьшенный размер окна

        selected_status = tk.StringVar(status_window)
        selected_status.set(status_options[0])

        status_menu = ttk.Combobox(status_window, textvariable=selected_status, values=status_options)
        status_menu.pack(pady=20)

        def confirm():
            new_status = selected_status.get()
            # Обновление статуса заявки в базе данных
            query = """
            UPDATE Request
            SET requestStatus = %s
            WHERE requestID = %s
            """
            self.db_cursor.execute(query, (new_status, request_id))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Статус заявки изменен!")
            self.load_requests()  # Обновляем таблицу заявок
            status_window.destroy()

        confirm_button = tk.Button(status_window, text="Подтвердить", command=confirm)
        confirm_button.pack(pady=10)

    def edit_request(self):
        # Выбор заявки для редактирования
        selected_item = self.requests_table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для редактирования.")
            return

        request_id = self.requests_table.item(selected_item)["values"][0]
        self.open_edit_window(request_id)

    def open_edit_window(self, request_id):
        # Окно для редактирования заявки
        edit_window = tk.Toplevel(self)
        edit_window.title("Редактировать заявку")
        edit_window.geometry("350x250")  # Уменьшенный размер окна

        # Загрузка данных о заявке из базы
        query = """
        SELECT orgTechType, orgTechModel, problemDescription
        FROM Request
        WHERE requestID = %s
        """
        self.db_cursor.execute(query, (request_id,))
        request = self.db_cursor.fetchone()

        if not request:
            messagebox.showerror("Ошибка", "Заявка не найдена.")
            edit_window.destroy()
            return

        org_tech_type, org_tech_model, problem_description = request

        tk.Label(edit_window, text="Вид оргтехники:").pack(pady=5)
        org_tech_type_entry = tk.Entry(edit_window)
        org_tech_type_entry.pack()
        org_tech_type_entry.insert(0, org_tech_type)

        tk.Label(edit_window, text="Модель:").pack(pady=5)
        org_tech_model_entry = tk.Entry(edit_window)
        org_tech_model_entry.pack()
        org_tech_model_entry.insert(0, org_tech_model)

        tk.Label(edit_window, text="Описание проблемы:").pack(pady=5)
        problem_description_entry = tk.Entry(edit_window)
        problem_description_entry.pack()
        problem_description_entry.insert(0, problem_description)

        def save_changes():
            new_org_tech_type = org_tech_type_entry.get()
            new_org_tech_model = org_tech_model_entry.get()
            new_problem_description = problem_description_entry.get()

            # Обновление данных заявки
            query = """
            UPDATE Request
            SET orgTechType = %s, orgTechModel = %s, problemDescription = %s
            WHERE requestID = %s
            """
            self.db_cursor.execute(query, (new_org_tech_type, new_org_tech_model, new_problem_description, request_id))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Заявка обновлена!")
            self.load_requests()  # Обновляем таблицу заявок
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.pack(pady=10)

    def assign_master(self):
        # Выбор заявки для назначения мастера
        selected_item = self.requests_table.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите заявку для назначения мастера.")
            return

        request_id = self.requests_table.item(selected_item)["values"][0]
        self.open_assign_master_window(request_id)



class AddRequestWindow(tk.Toplevel):
    def __init__(self, client_id, db_connection, update_callback):
        super().__init__()

        self.client_id = client_id
        self.db_connection = db_connection
        self.db_cursor = db_connection.cursor()
        self.update_callback = update_callback

        self.title("Добавить новую заявку")
        self.geometry("400x300")

        # Поля для добавления заявки
        tk.Label(self, text="Вид оргтехники").pack(pady=5)
        self.device_type_input = tk.Entry(self)
        self.device_type_input.pack(pady=5)

        tk.Label(self, text="Модель").pack(pady=5)
        self.model_input = tk.Entry(self)
        self.model_input.pack(pady=5)

        tk.Label(self, text="Описание проблемы").pack(pady=5)
        self.problem_input = tk.Entry(self)
        self.problem_input.pack(pady=5)

        # Кнопка для добавления заявки
        add_button = tk.Button(self, text="Добавить заявку", command=self.add_request)
        add_button.pack(pady=20)
    def add_request(self):
        device_type = self.device_type_input.get()
        model = self.model_input.get()
        problem = self.problem_input.get()

        if not all([device_type, model, problem]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Вставка заявки в базу данных
        query = """
        INSERT INTO Request (startDate, orgTechType, orgTechModel, problemDescription, requestStatus, clientID)
        VALUES (CURDATE(), %s, %s, %s, 'Новая заявка', %s)
        """
        self.db_cursor.execute(query, (device_type, model, problem, self.client_id))
        self.db_connection.commit()
        messagebox.showinfo("Успех", "Заявка добавлена!")
        self.update_callback()  # Обновляем таблицу заявок
        self.destroy()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()