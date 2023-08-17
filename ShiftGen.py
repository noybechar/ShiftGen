from main import *
import tkinter as tk
import sys
from tkinter import ttk, messagebox

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
The functions that describe what happens if ENTER or RANDOMIZE are being pressed.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def on_enter(event):
    # Check which priority is selected
    priority = priority_combobox.current()  # 0 for high, 1 for medium, 2 for low

    # Add worker to the list
    priority_num = ['High','Medium','Low']
    worker = worker_entry.get()
    if worker:
        workers_list[priority].append(worker)
        worker_entry.delete(0, tk.END)  # Clear the entry box
        table.insert('', 'end', values=(worker, priority_num[priority]), tags=(priority,))
############
def on_randomize():
    workers_in_one_list = []
    for i in range(3):
        for j in range(len(workers_list[i])):
            workers_in_one_list.append(workers_list[i][j])
    num_of_workers_total = len(workers_in_one_list)

    try:
        fairness_level = int(fairness_spinbox.get())
    except ValueError:
        messagebox.showinfo("Error", "Please change the fairness level into a number.")
        sys.exit()
    try:
        num_morning = int(morning_combobox.get())
    except ValueError:
        messagebox.showinfo("Error", "Please change the morning workers into a number.")
        sys.exit()

    try:
        num_afternoon = int(afternoon_combobox.get())
    except ValueError:
        messagebox.showinfo("Error", "Please change the afternoon workers into a number.")
        sys.exit()
    try:
        num_evening = int(evening_combobox.get())
    except ValueError:
        messagebox.showinfo("Error", "Please change the evening workers into a number.")
        sys.exit()

    if num_of_workers_total <= num_morning or num_of_workers_total \
            <= num_afternoon or num_of_workers_total <= num_evening:
        messagebox.showinfo("Error", "Not enough workers!")
        sys.exit()

    try:
        main(workers_list, fairness_level, num_morning, num_afternoon, num_evening)
        messagebox.showinfo("Success", "Successfully created the shifts!")

    except:
        messagebox.showinfo("Error","There is an unknown error.\nTry closing the new "
                                    "shifts file\nor shifts are impossible to make.")
        sys.exit()

    # try:
    #     main(workers_list,fairness_level,num_morning,num_afternoon,num_evening)
    #     messagebox.showinfo("Success", "Successfully created the shifts!")
    # except:
    #     messagebox.showinfo("Error","There is an unknown error.\nTry closing the new "
    #                                 "shifts file\nor shifts are impossible to make.")
    #     sys.exit()

"""""""""""""""""""""""""""
        The GUI
"""""""""""""""""""""""""""
textabout = open('abouttxt.txt','r')
texthowtouse = open('hottousetxt.txt','r')
app = tk.Tk()
app.title("ShiftGen - by Noy Bechar")
app.geometry("627x260")
app.resizable(0,0)
font_settings = ("Calibri", 12)

# Create a combobox for priority selection
priority_combobox = ttk.Combobox(app, values=["High priority", "Medium priority", "Low priority"], font=font_settings)
priority_combobox.grid(row=0, column=0, pady=5, padx=10, sticky="w")
priority_combobox.set("High priority")  # default value

# Create an entry box for worker's name
worker_entry = tk.Entry(app, font=font_settings)
worker_entry.grid(row=1, column=0, pady=5, padx=10, sticky="w")
worker_entry.bind('<Return>', on_enter)

# Spinbox for fairness level

values = ["Fairness level"] + list(range(0,21))
my_var= tk.StringVar(app)
fairness_spinbox = tk.Spinbox(app,values=values, textvariable=my_var,font=font_settings)
fairness_spinbox.grid(row=2, column=0, pady=5, padx=10, sticky="w")
my_var.set("Fairness level")

# Comboboxes for number of employees in each shift
morning_combobox = ttk.Combobox(app, values=list(range(1,11)), font=font_settings)
morning_combobox.grid(row=3, column=0, pady=5, padx=10, sticky="w")
morning_combobox.set('Morning Workers')  # default value

afternoon_combobox = ttk.Combobox(app, values=list(range(1,11)), font=font_settings)
afternoon_combobox.grid(row=4, column=0, pady=5, padx=10, sticky="w")
afternoon_combobox.set('Afternoon Workers')  # default value

evening_combobox = ttk.Combobox(app, values=list(range(1,11)), font=font_settings)
evening_combobox.grid(row=5, column=0, pady=5, padx=10, sticky="w")
evening_combobox.set('Evening Workers')  # default value

# "RANDOMIZE" button
randomize_btn = tk.Button(app, text="RANDOMIZE", command=on_randomize, font=font_settings)
randomize_btn.grid(row=6, column=0, pady=10, padx=10, sticky="w")


# List to hold workers based on priority
workers_list = [[], [], []]

# Table (Treeview) for displaying workers
table = ttk.Treeview(app, columns=('Worker', 'Priority'), show='headings')
table.heading('Worker', text='Worker Name')
table.heading('Priority', text='Priority')
table.grid(row=0, column=1, rowspan=7, padx=10, pady=10, sticky="nsew")
# table.bind('<Return>', on_enter)
# Applying color scheme
table.tag_configure(0, background="light coral")
table.tag_configure(1, background="light sky blue")
table.tag_configure(2, background="light green")

def onClickAbout():
    tk.messagebox.showinfo("About", textabout.read())

def onClickHowToUse():
    tk.messagebox.showinfo("How to use?", texthowtouse.read())

def outApp():
    app.quit()

# Menu
my_menu = tk.Menu(app)
app.config(menu=my_menu,bg='#4dbbd6')
help_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="How to use", command=onClickHowToUse)
help_menu.add_command(label="About", command=onClickAbout)
help_menu.add_separator()
help_menu.add_command(label="Exit", command=outApp)

app.mainloop()