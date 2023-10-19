import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

con = sqlite3.connect('emp.db')

class EmployeeManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Приложение компании")

        self.conn = sqlite3.connect('emp.db')
        self.create_table()

        #Создание таблицы с определёнными колонками
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Фио")
        self.tree.heading("Phone", text="телефон")
        self.tree.heading("Email", text="E-mail")
        self.tree.heading("Salary", text="Зарплата")
        self.tree.pack(padx=10, pady=10)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary INTEGER
            )
        ''')
        self.conn.commit()

        #Создание кнопок для реалезации функций
    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="Добавить сортудника", command=self.add_employee)
        self.add_button.pack(pady=5)
        self.update_button = tk.Button(self.master, text="Оновить информацию о сотруднике", command=self.update_employee)
        self.update_button.pack(pady=5)
        self.delete_button = tk.Button(self.master, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_button.pack(pady=5)
        self.search_button = tk.Button(self.master, text="Найти сотрудника", command=self.search_employee)
        self.search_button.pack(pady=5)

        #Функция просмотра Treewiew
        self.tree.bind("<Double-1>", self.on_double_click)

    #Добавление сотрудников
    def add_employee(self):
        name = simpledialog.askstring("Окно добавления", "Введите Фио сотрудника:")
        phone = simpledialog.askstring("Окно добавления", "Введите телефон сотрудника:")
        email = simpledialog.askstring("Окно добавления", "Введите почту сотрудника:")
        salary = simpledialog.askinteger("Окно добавления", "Введите зарпату сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO emp (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "add"
    
    #Обновление информации о сотрудниках
    def update_employee(self):
        emp_id = simpledialog.askinteger("Окно обновления", "Введите Id сотрудника")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM emp WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Окно обновления", "Введите обновлённое Фио:", initialvalue=employee[1])
            phone = simpledialog.askstring("Окно обновления", "Введите обновлённый телефон:", initialvalue=employee[2])
            email = simpledialog.askstring("Окно обновления", "Введите обновлённую почту:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Окно обновления", "Введите обновлённую зарпалту:", initialvalue=employee[4])

            cursor.execute("UPDATE emp SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = "update"
        else:
            messagebox.showerror("Ошибка обновления информации", "Сотрудник не найден.")
    
    #Удаление сотрудников
    def delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM emp WHERE id=?", (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "delete"


    
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM emp WHERE id=?", (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "delete"
    
    #Поиск сотрудников по Фио
    def search_employee(self):
        name = simpledialog.askstring("Поиск", "Введите фио сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM emp WHERE name=?", (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Информация", "Таких сотрудников нету.")

    #Очистка Treeview
    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM emp")
        emp = cursor.fetchall()

        for emp in emp:
            self.tree.insert("", "end", values=emp)
    
    #Выполнение функции при двойном нажатии
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        emp_id = self.tree.item(item, "values")[0]  #Получинение Id сотрудника
        messagebox.showinfo("Id сотрудника", f"Id сотрудника: {emp_id}")

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()