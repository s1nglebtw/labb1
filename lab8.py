import json
import os
from guizero import App, Box, Text, TextBox, PushButton, ListBox, Window, info, error, yesno

# --- исключения ---
class KanbanError(Exception):
    pass

class InvalidStatusError(KanbanError):
    pass

class TaskNotFoundError(KanbanError):
    pass

class DuplicateTaskError(KanbanError):
    pass


# --- Модель задачи ---
class Task:
    def __init__(self, title, description=""):
        if not title.strip():
            raise ValueError("Название задачи не может быть пустым.")
        self.title = title.strip()
        self.description = description

    def to_dict(self):
        return {"title": self.title, "description": self.description}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data.get("description", ""))


# --- Модель колонки ---
class Column:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        if any(t.title == task.title for t in self.tasks):
            raise DuplicateTaskError(f"Задача '{task.title}' уже существует в колонке '{self.name}'.")
        self.tasks.append(task)

    def remove_task(self, title: str):
        for i, t in enumerate(self.tasks):
            if t.title == title:
                return self.tasks.pop(i)
        raise TaskNotFoundError(f"Задача '{title}' не найдена в колонке '{self.name}'.")

    def get_task(self, title: str):
        for t in self.tasks:
            if t.title == title:
                return t
        raise TaskNotFoundError(f"Задача '{title}' не найдена.")


# --- Приложение ---
class KanbanApp:
    FILE = "kanban_ru.json"

    def __init__(self):
        self.columns = [
            Column("К выполнению"),
            Column("В процессе"),
            Column("Готово")
        ]

        self.app = App(title="Канбан-доска", width=950, height=500)
        self.listboxes = []

        self.build_gui()
        self.load()

    # --- Интерфейс ---
    def build_gui(self):
        top = Box(self.app, layout="grid")

        Text(top, text="Название:", grid=[0,0])
        self.title_in = TextBox(top, width=30, grid=[1,0])

        Text(top, text="Описание:", grid=[0,1])
        self.desc_in = TextBox(top, width=40, height=3, multiline=True, grid=[1,1])

        PushButton(top, text="Добавить", command=self.add_task, grid=[2,0])
        PushButton(top, text="Сохранить", command=self.save, grid=[2,1])

        Text(top, text="Поиск:", grid=[0,2])
        self.search_in = TextBox(top, width=30, grid=[1,2])
        PushButton(top, text="Фильтр", command=self.apply_filter, grid=[2,2])
        PushButton(top, text="Сброс", command=self.refresh, grid=[3,2])

        # --- Выровненные колонки ---
        area = Box(self.app, layout="grid")

        for i, col in enumerate(self.columns):
            frame = Box(area, border=True, layout="grid", width=300, height=380, grid=[i,0])

            # Заголовок колонки
            Text(frame, text=col.name, size=14, grid=[0,0])

            # Список задач
            lb = ListBox(frame, items=[], width="fill", height="fill", grid=[0,1])
            lb.when_double_clicked = self.view_task_factory(i)
            self.listboxes.append(lb)

            # Кнопки управления
            btns = Box(frame, layout="grid", grid=[0,2])
            PushButton(btns, text="Изменить", command=self.edit_task_factory(i), grid=[0,0])
            PushButton(btns, text="Удалить", command=self.delete_task_factory(i), grid=[1,0])
            PushButton(btns, text="←", command=self.move_left_factory(i), grid=[0,1])
            PushButton(btns, text="→", command=self.move_right_factory(i), grid=[1,1])

    # --- Фабрики действий ---
    def view_task_factory(self, i):
        def fn():
            lb = self.listboxes[i]
            sel = lb.value
            if not sel:
                info("Ошибка", "Выберите задачу.")
                return
            task = self.columns[i].get_task(sel)

            w = Window(self.app, title=task.title, width=400, height=300)
            Text(w, text="Название:")
            Text(w, text=task.title)
            Text(w, text="Описание:")
            Text(w, text=task.description)
        return fn

    def edit_task_factory(self, i):
        def fn():
            lb = self.listboxes[i]
            sel = lb.value
            if not sel:
                info("Ошибка", "Выберите задачу.")
                return
            task = self.columns[i].get_task(sel)

            w = Window(self.app, title="Изменить задачу", width=400, height=300)
            Text(w, text="Название:")
            t_in = TextBox(w, text=task.title, width=30)

            Text(w, text="Описание:")
            d_in = TextBox(w, text=task.description, width=40, height=4, multiline=True)

            def save_edit():
                new_title = t_in.value.strip()
                if not new_title:
                    error("Ошибка", "Название пустое.")
                    return
                if new_title != task.title and any(t.title == new_title for t in self.columns[i].tasks):
                    error("Ошибка", "Такая задача уже существует.")
                    return

                task.title = new_title
                task.description = d_in.value
                self.refresh()
                w.destroy()

            PushButton(w, text="Сохранить", command=save_edit)
        return fn

    def delete_task_factory(self, i):
        def fn():
            lb = self.listboxes[i]
            sel = lb.value
            if not sel:
                info("Ошибка", "Выберите задачу.")
                return
            if not yesno("Подтверждение", f"Удалить '{sel}'?"):
                return

            self.columns[i].remove_task(sel)
            self.refresh()
        return fn

    def move_left_factory(self, i):
        def fn():
            if i == 0:
                info("Ошибка", "Это крайняя левая колонка.")
                return
            lb = self.listboxes[i]
            sel = lb.value
            if not sel:
                info("Ошибка", "Выберите задачу.")
                return

            task = self.columns[i].remove_task(sel)
            self.columns[i-1].add_task(task)
            self.refresh()
        return fn

    def move_right_factory(self, i):
        def fn():
            if i == len(self.columns)-1:
                info("Ошибка", "Это крайняя правая колонка.")
                return
            lb = self.listboxes[i]
            sel = lb.value
            if not sel:
                info("Ошибка", "Выберите задачу.")
                return

            task = self.columns[i].remove_task(sel)
            self.columns[i+1].add_task(task)
            self.refresh()
        return fn

    # --- Логика ---
    def add_task(self):
        title = self.title_in.value.strip()
        desc = self.desc_in.value.strip()

        if not title:
            error("Ошибка", "Название задачи обязательно.")
            return

        task = Task(title, desc)
        self.columns[0].add_task(task)

        self.title_in.value = ""
        self.desc_in.value = ""
        self.refresh()

    def apply_filter(self):
        q = self.search_in.value.lower().strip()
        for i, col in enumerate(self.columns):
            lb = self.listboxes[i]
            lb.clear()

            for t in col.tasks:
                if q in t.title.lower():
                    lb.append(t.title)

    def refresh(self):
        for i, col in enumerate(self.columns):
            lb = self.listboxes[i]
            lb.clear()
            for t in col.tasks:
                lb.append(t.title)

    # --- Сохранение / загрузка ---
    def save(self):
        data = {
            "columns": [
                {"name": col.name, "tasks": [t.to_dict() for t in col.tasks]}
                for col in self.columns
            ]
        }

        with open(self.FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        info("Успех", "Доска сохранена.")

    def load(self):
        if not os.path.exists(self.FILE):
            return
        with open(self.FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.columns = []
        for col_data in data["columns"]:
            col = Column(col_data["name"])
            for t_data in col_data["tasks"]:
                col.tasks.append(Task.from_dict(t_data))
            self.columns.append(col)

        self.refresh()

    def run(self):
        self.app.display()


# --- Запуск ---
if __name__ == "__main__":
    KanbanApp().run()