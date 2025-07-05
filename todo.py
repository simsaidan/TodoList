"""
Author: Aidan Sims
"""


"""import tkinter for building GUI, sqlite3 for storing to-do items in database."""
import tkinter as tk
import sqlite3

# Connect to the database.
conn = sqlite3.connect("todo.sqlite")
cur = conn.cursor()


class TaskList:
    def __init__(self):
        """Initialize the TaskList by loading tasks from the database.
        Tasks are stored in the self.tasks attribute.
        Parameters: None
        """
        self.tasks = []
        rows = cur.execute("SELECT * from items").fetchall()
        for row in rows:
            self.tasks.append(row[0])
        self.num_items = len(self.tasks)

    def insert(self, t):
        """Adds a task to the list, persisting it in the database.
        Duplicate tasks are ignored.

        Parameters:
        t - The task to add (string)

        Returns True if added, False if task was already in the list."""
        if t in self.tasks:
            return False
        else:
            self.tasks.append(t)
            cur.execute("INSERT into items(tasks) values (?)", (t,))
            conn.commit()
            self.num_items += 1
            num_label.config(text="Number of items: " + str(self.num_items))
            return True

    def get_tasks(self):
        """Returns the tasks"""
        return self.tasks

    def get_num_items(self):
        """Return the number of items in the todo list"""
        return self.num_items

    def remove(self, t):
        """Removes a task from the list, deleting it from the database.
        If the task is not present, does nothing.
        Parameters:

        t - The task to remove (string)

        Returns True if the task was removed,
        False if it was not in the list."""
        if t in self.tasks:
            self.tasks.remove(t)
            cur.execute("Delete from items where tasks = (?)", (t,))
            conn.commit()
            self.num_items -= 1
            num_label.config(text="Number of items: " + str(self.num_items))
            return True
        else:
            return False


    def clear(self):
        """Clears all tasks from the list,
        removing them from the database as well."""
        self.tasks = []
        cur.execute("Delete from items")
        conn.commit()
        self.num_items = 0
        num_label.config(text="Number of items: " + str(self.num_items))


# TaskList for the todo-list
tasks = TaskList()

# GUI Window
window = tk.Tk()
window.geometry("400x300")
window.title("Aidan's Todo List")
input = tk.Entry(window)
input.pack()

# A place to pack everything
frame = tk.Frame(window)
frame.pack()

# Label to display the number of items
num_label = tk.Label(window, text="Number of items: " + str(tasks.get_num_items()))
num_label.pack()

# Text to display messages
text = tk.Label(fg="red")
text.pack()
text.config(text="")


def clear_message():
    """Clears the text of the text label."""
    text.config(text="")


def display(message):
    """Display a message on the screen
    Clear the message after 1300 milliseconds

    Parameters: message - The string message to display
    """
    text.config(text=message)
    window.after(1300, clear_message)


def submit():
    """Add a task to the to-do list"""
    task = input.get()
    if task == "":
        return
    r = tasks.insert(task)
    if not r:
        display("Task is already in the list")
    input.delete(0, "end")
    list.delete(0, "end")
    for task in tasks.get_tasks():
        list.insert("end", task)
    return


def delete():
        """Remove a task from the todo-list."""
        try:
            selected_task_index = list.curselection()[0]
            selected_task = list.get(selected_task_index)
            r = tasks.remove(selected_task)
            if not r:
                display("Task not in list")

            list.delete(selected_task_index)
            input.delete(0, "end")
        except IndexError:
            display("No task selected")


def clear_list():
    """Clears the todo list and removes all task"""
    list.delete(0, "end")
    tasks.clear()


# Button to submit a task
btn = tk.Button(frame, text="Submit", command=submit)
btn.pack(side="left", pady=10)

# Button to clear the list
btnd = tk.Button(frame, text="Clear", command=clear_list)
btnd.pack(side="right", pady=10)

# Button to delete an element
btnd = tk.Button(frame, text="Delete", command=delete)
btnd.pack(side="right", pady=10)

# Add tasks to window
list = tk.Listbox(window)
for task in tasks.get_tasks():
    list.insert("end", task)
list.pack()

tk.mainloop()
