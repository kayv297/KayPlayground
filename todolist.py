import tkinter as tk

def add_task():
    task = task_entry.get()
    if task != "":
        listbox_tasks.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        pass

def delete_task():
    try:
        index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(index)
    except IndexError:
        pass

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Create the entry widget for adding new tasks
task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

# Create the Add Task button
add_task_btn = tk.Button(root, text="Add Task", width=48, command=add_task)
add_task_btn.pack(pady=5)

# Create the listbox widget to display tasks
listbox_tasks = tk.Listbox(root, width=50, height=10)
listbox_tasks.pack(pady=10)

# Create the Delete Task button
delete_task_btn = tk.Button(root, text="Delete Task", width=48, command=delete_task)
delete_task_btn.pack(pady=5)

# Start the main event loop
root.mainloop()