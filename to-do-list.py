import tkinter as tk
from tkinter import messagebox
import sqlite3

# creating a database with sqlite3
def create_connection():
    try:
        conn = sqlite3.connect('todo_list_db.db')
        return conn

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")

        return None


# table in the database
def create_table():
    conn = create_connection()

    if conn:
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY,
                            task TEXT NOT NULL,
                            status TEXT NOT NULL)''')

            conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating table: {e}")
        finally:
            conn.close()


#task get added in list
def add_task(task):
    if task:
        conn = create_connection()

        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, 'PENDING'))
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "TASK ADDED IN LIST...")

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error adding task: {e}")
                conn.close()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")


# taking the tasks in the list from the table

def get_tasks(search_query=""):
    conn = create_connection()
    tasks = []

    if conn:
        try:
            c = conn.cursor()

            if search_query:
                c.execute("SELECT * FROM tasks WHERE task LIKE ? OR status LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
            else:
                c.execute("SELECT * FROM tasks")
            tasks = c.fetchall()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching tasks: {e}")

        finally:
            conn.close()
    return tasks


#status will be updated of selected task

def update_task_status(task_id, new_status):
    conn = create_connection()

    if conn:
        try:
            c = conn.cursor()
            c.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating task: {e}")
            conn.close()

#task deletion selected task

def delete_task(task_id):
    conn = create_connection()

    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting task: {e}")
            conn.close()

# frame for GUI
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List And Tasks")
        self.root.geometry("1050x550")
        self.root.config(bg="#f5f5f5")

        # Create a frame for the search bar and button
        self.search_boxs = tk.Frame(self.root, bg="#f5f5f5")
        self.search_boxs.pack(pady=10)

        self.search_entry = tk.Entry(self.search_boxs, width=40, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=10)

        self.search_button = tk.Button(self.search_boxs, text="SEARCH", width=15, font=("Times New Roman", 12), bg="#2196F3", fg="white", command=self.search_task)
        self.search_button.pack(side=tk.LEFT)

        # Create a frame for the listbox and scrollbar
        self.list_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.list_frame, height=10, width=50, selectmode=tk.SINGLE, font=("Arial", 12), bd=2)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.entry_box = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.entry_box.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="ADD", width=15, font=("Times New Roman", 12), bg="#A52A2A", fg="white", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="DELETE", width=15, font=("Times New Roman", 12), bg="#f44336", fg="white", command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.update_button = tk.Button(self.button_frame, text="UPDATE", width=15, font=("Times New Roman", 12), bg="#00008B", fg="white", command=self.update_status)
        self.update_button.grid(row=1, column=0, padx=10)

        self.mark_done_button = tk.Button(self.button_frame, text="MARK DONE", width=15, font=("Times New Roman", 12), bg="#FF9800", fg="white", command=self.mark_done)
        self.mark_done_button.grid(row=1, column=1, padx=10)

        # PRESS "ENTER" TO ADD IN LIST
        self.entry_box.bind("<Return>", self.on_enter_press)

        # collecting the task
        self.refresh_tasks()

    def on_enter_press(self, event=None):
        task = self.entry_box.get()
        if task:
            add_task(task)
            self.refresh_tasks()
            self.entry_box.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "ENTER A TASK PLEASE.")

    def add_task(self):
        task = self.entry_box.get()
        if task:
            add_task(task)
            self.refresh_tasks()
            self.entry_box.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "ENTER A TASK PLEASE")

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks()
        for idx, task in enumerate(tasks, 1):
            task_id = task[0]
            task_name = task[1]
            task_status = task[2]
            self.task_listbox.insert(tk.END, f"{task_id}. {task_name} [{task_status}]")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_text = self.task_listbox.get(selected_index)
            task_id = int(task_text.split(".")[0])
            delete_task(task_id)
            self.refresh_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "SELECT A TASK TO DELETE PLEASE.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_status(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_text = self.task_listbox.get(selected_index)
            task_id = int(task_text.split(".")[0])

            # Check the status and change between Pending/Completed
            if "PENDING" in task_text:
                new_status = "COMPLETED"
            else:
                new_status = "PENDING"

            update_task_status(task_id, new_status)
            self.refresh_tasks()

        except IndexError:
            messagebox.showwarning("Selection Error", "SELECT A TASK TO INPUT PLEASE")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def mark_done(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_text = self.task_listbox.get(selected_index)
            task_id = int(task_text.split(".")[0])

            # Mark task as done (Completed)
            update_task_status(task_id, "COMPLETED")
            self.refresh_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "SELECT A TASK TO MARK IT DONE")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def search_task(self):
        search_query = self.search_entry.get()
        if search_query:
            self.task_listbox.delete(0, tk.END)
            tasks = get_tasks(search_query)
            for idx, task in enumerate(tasks, 1):
                task_id = task[0]
                task_name = task[1]
                task_status = task[2]
                self.task_listbox.insert(tk.END, f"{task_id}. {task_name} [{task_status}]")
        else:
            messagebox.showwarning("Input Error", "ENTER SOMETHING TO SEARCH")

if __name__ == "__main__":
    create_table()  # creating database
    root = tk.Tk()  # frame calling
    app = TodoApp(root)
    root.mainloop() # to make it stable
