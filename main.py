import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")

        # Предопределённые задачи с типами
        self.predefined_tasks = [
            {"task": "Прочитать статью", "type": "учёба"},
            {"task": "Сделать зарядку", "type": "спорт"},
            {"task": "Написать отчёт", "type": "работа"},
            {"task": "Решить задачу", "type": "учёба"},
            {"task": "Погулять на улице", "type": "спорт"},
            {"task": "Подготовить презентацию", "type": "работа"},
        ]

        self.history = self.load_history()

        # Поле для отображения задачи
        self.task_label = tk.Label(root, text="Нажмите 'Сгенерировать задачу'", font=('Arial', 14))
        self.task_label.pack(pady=10)

        # Кнопка генерации
        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        # Фильтр по типу
        self.filter_var = tk.StringVar(value="все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        tk.OptionMenu(filter_frame, self.filter_var, "все", "учёба", "спорт", "работа", command=self.update_history_list).pack(side=tk.LEFT)

        # Список истории
        self.history_listbox = tk.Listbox(root, width=50, height=10)
        self.history_listbox.pack(pady=10)

        # Кнопка добавления задачи
        self.add_entry = tk.Entry(root, width=30)
        self.add_entry.pack(pady=5)
        self.add_btn = tk.Button(root, text="Добавить свою задачу", command=self.add_custom_task)
        self.add_btn.pack(pady=5)

        # Кнопка сохранения истории
        self.save_btn = tk.Button(root, text="Сохранить историю", command=self.save_history)
        self.save_btn.pack(pady=5)

        # Обновление списка истории
        self.update_history_list()

    def generate_task(self):
        task = random.choice(self.predefined_tasks)
        self.task_label.config(text=f"Задача: {task['task']} (тип: {task['type']})")
        self.history.append(task)
        self.update_history_list()

    def add_custom_task(self):
        task_text = self.add_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Ошибка", "Введите задачу!")
            return
        task_type = simpledialog.askstring("Тип задачи", "Введите тип задачи (учёба/спорт/работа):")
        if task_type not in ["учёба", "спорт", "работа"]:
            messagebox.showerror("Ошибка", "Некорректный тип задачи!")
            return
        new_task = {"task": task_text, "type": task_type}
        self.predefined_tasks.append(new_task)
        self.history.append(new_task)
        self.update_history_list()
        self.add_entry.delete(0, tk.END)

    def update_history_list(self, *args):
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        for item in self.history:
            if filter_type == "все" or item["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{item['task']} (тип: {item['type']})")

    def save_history(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "История сохранена!")

    def load_history(self):
        if not os.path.exists("tasks.json"):
            return []
        with open("tasks.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
