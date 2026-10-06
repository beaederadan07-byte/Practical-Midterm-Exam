import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect("artist.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")

conn.commit()


def add_artist():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    genre = genre_entry.get().strip()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            
        )
        return

    try:
        age = int(age)

        if age < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            
        )
        return

    cursor.execute(
        "INSERT INTO artist (name, age, genre) VALUES (?, ?, ?)",
        (name, age, genre)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        
    )

    clear_fields()
    display_artist()



def display_artist():
    
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM artist")
    artists = cursor.fetchall()

    for artist in artists:
        tree.insert(
            "",
            tk.END,
            values=artist
        )




def update_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            
        )
        return

    artist_id = tree.item(selected[0])["values"][0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    genre = genre_entry.get().strip()

    if name == "" or age == "" or genre == "":
        messagebox.showwarning(
            "Warning",
            
        )
        return

    try:
        age = int(age)

        if age < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            
        )
        return

    cursor.execute("""
        UPDATE artist
        SET name = ?, age = ?, genre = ?
        WHERE id = ?
    """, (name, age, genre, artist_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
       
    )

    clear_fields()
    display_artist()




def delete_artist():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
        
        )
        return

    artist_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        
    )

    if confirm:
        cursor.execute(
            "DELETE FROM artist WHERE id = ?",
            (artist_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
           
        )

        clear_fields()
        display_artist()




def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)

    if tree.selection():
        tree.selection_remove(tree.selection())




def select_artist(event):
    selected = tree.selection()

    if selected:
        artist = tree.item(selected[0])["values"]

        clear_fields()

        name_entry.insert(0, artist[1])
        age_entry.insert(0, artist[2])
        genre_entry.insert(0, artist[3])



root = tk.Tk()

root.title("Song Artist Information")
root.geometry("750x600")
root.configure(bg="#EAF4FB")

BG_COLOR = "#EAF4FB"
TITLE_COLOR = "#154360"
LABEL_COLOR = "#1F618D"
ENTRY_BG = "#FFFFFF"

ADD_COLOR = "#27AE60"
UPDATE_COLOR = "#F39C12"
DELETE_COLOR = "#E74C3C"
CLEAR_COLOR = "#7F8C8D"

BUTTON_TEXT = "white"



title_label = tk.Label(
    root,
    text="Song Artist Information",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack(pady=15)




input_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="groove"
)

input_frame.pack(
    pady=5,
    padx=20,
    fill="x"
)




tk.Label(
    input_frame,
    text="Artist Name:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)


name_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)




tk.Label(
    input_frame,
    text="Age:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)


age_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

age_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)




tk.Label(
    input_frame,
    text="Genre:",
    font=("Arial", 11, "bold"),
    bg="white",
    fg=LABEL_COLOR
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="e"
)


genre_entry = tk.Entry(
    input_frame,
    width=35,
    font=("Arial", 11),
    bg=ENTRY_BG,
    fg="#212121",
    relief="solid",
    bd=1
)

genre_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)




button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(pady=15)




tk.Button(
    button_frame,
    text="Add",
    width=12,
    font=("Arial", 10, "bold"),
    bg=ADD_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#1E8449",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_artist
).grid(
    row=0,
    column=0,
    padx=5
)




tk.Button(
    button_frame,
    text="Update",
    width=12,
    font=("Arial", 10, "bold"),
    bg=UPDATE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#D68910",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=update_artist
).grid(
    row=0,
    column=1,
    padx=5
)




tk.Button(
    button_frame,
    text="Delete",
    width=12,
    font=("Arial", 10, "bold"),
    bg=DELETE_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#C0392B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=delete_artist
).grid(
    row=0,
    column=2,
    padx=5
)




tk.Button(
    button_frame,
    text="Clear",
    width=12,
    font=("Arial", 10, "bold"),
    bg=CLEAR_COLOR,
    fg=BUTTON_TEXT,
    activebackground="#626567",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)



style = ttk.Style()

style.theme_use("clam")


style.configure(
    "Treeview.Heading",
    background="#1F618D",
    foreground="white",
    font=("Arial", 10, "bold"),
    padding=8
)


style.configure(
    "Treeview",
    background="white",
    foreground="#212121",
    rowheight=30,
    fieldbackground="white",
    font=("Arial", 10)
)


style.map(
    "Treeview",
    background=[
        ("selected", "#5DADE2")
    ],
    foreground=[
        ("selected", "white")
    ]
)




tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Genre"),
    show="headings"
)


tree.heading(
    "ID",
    text="ID"
)

tree.heading(
    "Name",
    text="Artist Name"
)

tree.heading(
    "Age",
    text="Age"
)

tree.heading(
    "Genre",
    text="Genre"
)


tree.column(
    "ID",
    width=60,
    anchor="center"
)

tree.column(
    "Name",
    width=250
)

tree.column(
    "Age",
    width=80,
    anchor="center"
)

tree.column(
    "Genre",
    width=220
)


tree.tag_configure(
    "evenrow",
    background="#F4F9FC"
)

tree.tag_configure(
    "oddrow",
    background="#D6EAF8"
)


tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)




tree.bind(
    "<<TreeviewSelect>>",
    select_artist
)




display_artist()




root.mainloop()



conn.close()
