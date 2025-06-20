import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.factory import Factory
import json
import os

# Load the KV file
Builder.load_file("todo.kv")

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

class TaskPopup(Popup):
    task_input = ObjectProperty(None)
    confirm_callback = ObjectProperty(None)

    def on_open(self):
        self.task_input.focus = True

    def add_task(self):
        text = self.task_input.text.strip()
        if text:
            self.confirm_callback(text)
            self.dismiss()

class TodoWidget(BoxLayout):
    task_input = ObjectProperty(None)
    tasks_list = ObjectProperty(None)
    tasks = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = load_tasks()

    def add_task(self):
        popup = TaskPopup(confirm_callback=self.confirm_add_task)
        popup.open()

    def confirm_add_task(self, text):
        self.tasks.append({'text': text, 'done': False})
        self.save_and_refresh()

    def remove_task(self, idx):
        self.tasks.pop(idx)
        self.save_and_refresh()

    def toggle_task(self, idx):
        self.tasks[idx]['done'] = not self.tasks[idx]['done']
        self.save_and_refresh()

    def save_and_refresh(self):
        save_tasks(self.tasks)
        self.tasks = self.tasks[:]  # Trigger update

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t['done']]
        self.save_and_refresh()

    def update_tasks_list(self):
        self.ids.tasks_list.clear_widgets()
        for idx, task in enumerate(self.tasks):
            item = Factory.TaskItem(
                task_text=task['text'],
                done=task['done'],
                idx=idx,
                toggle_callback=self.toggle_task,
                remove_callback=self.remove_task
            )
            self.ids.tasks_list.add_widget(item)

class TodoApp(App):
    def build(self):
        return TodoWidget()

if __name__ == "__main__":
    TodoApp().run()
