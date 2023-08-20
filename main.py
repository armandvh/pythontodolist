from tkinter import *
from tkcalendar import *
from tkinter import ttk
import sqlite3
# Making a small window
window = Tk()
window.title("Productive ToDoList Using Python")
window.geometry("800x600")
window.minsize(600,200)
window.resizable(width=False,height=True)
#End of Configuration of Window

#Database Configuration
task_datas = sqlite3.connect("test.db")
task_cursor = task_datas.cursor()
task_cursor.execute("CREATE TABLE IF NOT EXISTS tasks(task, time, priority , category) ")
#End of Database Configuration

#Creating the functions of the ToDoList
def add_task():
    tasks_list.insert(END,"Task: "+task_entry.get()+" Due Time: "+date_entry.get()+" Priority: "+priority_combobox.get()+" Category: "+category_entry.get())
    task_cursor.execute("INSERT INTO tasks(task , time ,priority , category) VALUES (?,?,?,?)",(task_entry.get() , date_entry.get() , priority_combobox.get() , category_entry.get()))
    task_datas.commit()
def delete_task():
    temp_index = tasks_list.curselection()
    if temp_index:
        selected_index = temp_index[0]
        tasks_list.delete(selected_index)
        task_cursor.execute("SELECT rowid FROM tasks LIMIT 1 OFFSET ?", (selected_index,))
        selected_id = task_cursor.fetchone()[0]
        task_cursor.execute("DELETE FROM tasks WHERE rowid=?", (selected_id,))
        task_datas.commit()

def load_task():
    task_cursor.execute("SELECT * FROM tasks")
    temp = task_cursor.fetchall()
    tasks_list.delete(0,END)
    for row in temp:
        tasks_list.insert(END,"Task: "+ row[0] + " Due Time: " + row[1] + " Priority: " + row[2] + " Category: " + row[3])
        task_datas.commit()
#The Functions end here

#Creating the GUI and FORMS for the ToDoList

task_label = Label(window, text="Task: ")
task_entry = Entry(window)

task_label.grid(row = 0 , column = 0 , pady = 2,padx=(0,5) , sticky= "e")
task_entry.grid(row = 0 , column =1 , pady = 2,padx=(0,0) , sticky="w")



duetime_label = Label(window, text="Due time:")
duetime_label.grid(row = 1, column =0 , pady = 2 ,padx=(0,5) , sticky = "e")

date_entry = DateEntry(window, locale='en_US', date_pattern='mm/dd/y')
date_entry.grid(row= 1 , column = 1 , pady = 2 , padx=(0,0), sticky="w")

task_priority = Label(window, text="Priority: ")
task_priority.grid(row = 2 , column = 0 , pady = 2 , padx=(0,5),sticky="e")

priority_stringvar = StringVar()
priority_combobox = ttk.Combobox(window , textvariable=priority_stringvar ,state="readonly")
priority_combobox["values"] = ("low",
                               "medium",
                               "high")
priority_combobox.grid(row = 2, column =1 , pady =2, padx=(0,0) , sticky="w")

category_label = Label(window, text="Category")
category_label.grid(row=3 , column=0 ,pady=2 , padx=(0,5), sticky="e")

category_entry = Entry(window)
category_entry.grid(row=3 , column=1,pady = 2 , padx=(0,0) , sticky="w")

add_button = Button(window , text="Add Task" , command=add_task)
add_button.grid(row=4 , column = 0 , pady=2 , padx=(5,0))
remove_button = Button(window, text="Remove Task", command=delete_task)
remove_button.grid(row=4 , column = 1 , pady =2 , padx = (0,0))
load_button = Button(window, text="Load Task" , command=load_task)
load_button.grid(row=4 , column =2 , pady = 2 , padx=(0,0))


tasks_list = Listbox(window,width= 50)
tasks_list.grid(row=0 , column = 3 , rowspan= 5 , pady = 2 , padx=(20,0),sticky="s")
#The GUI Finishes here
window.mainloop()
