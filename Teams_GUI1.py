import sqlite3
from tkinter import *
from tkinter import messagebox
import Teams_GUI2 as dialog_module

DB_PATH = "TeamsData.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def fetch_all_teams():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM Teams")
    rows = cur.fetchall()
    con.close()
    return rows

def fetch_distinct(field):
    con = get_connection()
    cur = con.cursor()
    cur.execute(f"SELECT DISTINCT {field} FROM Teams ORDER BY {field}")
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows

def fetch_by_city(city):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM Teams WHERE city = ?", (city,))
    rows = cur.fetchall()
    con.close()
    return rows

def fetch_by_division(div):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM Teams WHERE division = ?", (div,))
    rows = cur.fetchall()
    con.close()
    return rows

def update_points_in_db(team_name, new_points, new_avg):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE Teams SET points = ?, rating = ? WHERE team = ?", (new_points, new_avg, team_name))
    con.commit()
    con.close()

def insert_team_to_db(team_tuple):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO Teams VALUES(?,?,?,?,?,?,?,?,?,?)", team_tuple)
    con.commit()
    con.close()

def delete_team_in_db(team_name):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM Teams WHERE team = ?", (team_name,))
    con.commit()
    con.close()

root = Tk()
root.title("NBA Basketball Teams")
root.geometry("760x520")
root.resizable(False, False)
root.configure(bg="#062f2f")

LABEL_BG = "#0b525b"
ENTRY_BG = "#e6f6f5"
ACCENT = "#ffd166"
FONT_HEADING = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 10, "bold")
FONT_BTN = ("Helvetica", 10, "bold")

current_index = 0

admin_mb = Menubutton(root, text="Admin", relief=RAISED, bg="#062f2f", fg=ACCENT, font=FONT_LABEL)
admin_menu = Menu(admin_mb, tearoff=0)
admin_mb.config(menu=admin_menu)
admin_menu.add_command(label="Delete Team", command=lambda: delete_current_team())
admin_mb.place(x=6, y=10)

heading = Label(root, text="NBA Basketball Teams", font=FONT_HEADING, fg=ACCENT, bg="#062f2f")
heading.place(x=86, y=10)

frm = Frame(root, bg=LABEL_BG, bd=0)
frm.place(x=18, y=50, width=360, height=440)

frm_right = Frame(root, bg="#0a3839")
frm_right.place(x=400, y=50, width=340, height=440)

def make_label(master, text, r, c):
    lbl = Label(master, text=text, bg=LABEL_BG, fg="white", font=FONT_LABEL, anchor="w")
    lbl.grid(row=r, column=c, padx=(12,4), pady=8, sticky="w")
    return lbl

def make_entry(master, r, c, width=24):
    e = Entry(master, width=width, bg=ENTRY_BG, bd=2)
    e.grid(row=r, column=c, padx=(4,12), pady=8, sticky="w")
    return e

frm.grid_rowconfigure(9, weight=1)

make_label(frm, "Team:", 0, 0)
entry_team = make_entry(frm, 0, 1)

make_label(frm, "Coach:", 1, 0)
entry_coach = make_entry(frm, 1, 1)

make_label(frm, "City:", 2, 0)
entry_city = make_entry(frm, 2, 1)

make_label(frm, "Wins:", 3, 0)
entry_wins = make_entry(frm, 3, 1, width=10)

make_label(frm, "Losses:", 4, 0)
entry_losses = make_entry(frm, 4, 1, width=10)

make_label(frm, "Points:", 5, 0)
entry_points = make_entry(frm, 5, 1, width=12)

make_label(frm, "Avg Points:", 6, 0)
entry_avg = make_entry(frm, 6, 1, width=12)
entry_avg.config(state='readonly')

make_label(frm, "Divisions:", 7, 0)
division_var = StringVar()
division_dropdown = OptionMenu(frm, division_var, "")
division_dropdown.grid(row=7, column=1, padx=(4,12), pady=8, sticky="w")
division_var.set("")

made_playoffs_var = IntVar(value=0)
cb_playoff = Checkbutton(frm, text="Made Playoffs", variable=made_playoffs_var, bg=LABEL_BG, fg="white", command=lambda: on_playoff_toggle())
cb_playoff.grid(row=8, column=0, columnspan=2, pady=6, padx=12, sticky="w")

lbl_desc = Label(frm, text="Description (Arena):", bg=LABEL_BG, fg="white", font=FONT_LABEL)
lbl_desc.grid(row=9, column=0, padx=(12,4), pady=(8,4), sticky="nw")
text_description = Text(frm, height=4, width=28, bg=ENTRY_BG)
text_description.grid(row=9, column=1, padx=(4,12), pady=(8,4), sticky="w")

btn_next = Button(frm, text="Next", font=FONT_BTN, bg=ACCENT, command=lambda: next_entry(), width=12)
btn_next.grid(row=11, column=0, padx=12, pady=8, sticky="w")

btn_prev = Button(frm, text="Prev", font=FONT_BTN, bg=ACCENT, command=lambda: prev_entry(), width=12)
btn_prev.grid(row=11, column=1, padx=12, pady=8, sticky="e")

btn_clear = Button(frm, text="Clear", font=FONT_BTN, bg="#d4a373", command=lambda: clear_form(), width=12)
btn_clear.grid(row=12, column=0, padx=12, pady=8, sticky="w")

btn_insert = Button(frm, text="Insert", font=FONT_BTN, bg="#d4a373", command=lambda: insert_cmd(), width=12)
btn_insert.grid(row=12, column=1, padx=12, pady=8, sticky="e")

lbl_add = Label(frm_right, text="Add Points", bg="#0a3839", fg=ACCENT, font=FONT_LABEL)
lbl_add.place(x=18, y=18)

add_points_var = StringVar()
add_points_options = ["1", "2", "5", "10"]
add_points_var.set(add_points_options[0])
opt_addpoints = OptionMenu(frm_right, add_points_var, *add_points_options)
opt_addpoints.place(x=20, y=50)

def addpoints_cmd():
    team_name = entry_team.get().strip()
    if not team_name:
        return
    try:
        add_val = int(add_points_var.get())
    except:
        messagebox.showerror("Invalid", "Addpoints selection invalid.")
        return
    try:
        cur_points = int(entry_points.get() or "0")
    except:
        cur_points = 0
    new_points = cur_points + add_val
    try:
        wins = int(entry_wins.get() or "0")
    except:
        wins = 0
    new_avg = round(new_points / (wins if wins>0 else 1), 2)
    entry_points.delete(0, END)
    entry_points.insert(END, str(new_points))
    entry_avg.config(state='normal')
    entry_avg.delete(0, END)
    entry_avg.insert(END, str(new_avg))
    entry_avg.config(state='readonly')
    update_points_in_db(team_name, new_points, new_avg)

btn_addpoints = Button(frm_right, text="AddPoints", bg=ACCENT, font=FONT_BTN, command=addpoints_cmd)
btn_addpoints.place(x=120, y=46, width=180)

lbl_showall = Label(frm_right, text="Search Database", bg="#0a3839", fg=ACCENT, font=FONT_LABEL)
lbl_showall.place(x=18, y=110)

def show_all_cmd():
    rows = fetch_all_teams()
    dialog_module.displayDialog(root, rows)

btn_showall = Button(frm_right, text="Show All", bg="#ffd6a5", font=FONT_BTN, command=show_all_cmd)
btn_showall.place(x=20, y=140, width=160)

city_var = StringVar()
city_var.set("")
cities = fetch_distinct("city")
city_menu = OptionMenu(frm_right, city_var, *cities) if cities else OptionMenu(frm_right, city_var, "")
city_menu.place(x=20, y=200, width=160)
lbl_city = Label(frm_right, text="City", bg="#0a3839", fg="white")
lbl_city.place(x=20, y=176)

def show_by_city_cmd():
    sel = city_var.get()
    if not sel:
        return
    rows = fetch_by_city(sel)
    dialog_module.displayDialog(root, rows)

btn_showcity = Button(frm_right, text="Show By City", bg="#ffd6a5", font=FONT_BTN, command=show_by_city_cmd)
btn_showcity.place(x=190, y=200, width=130)

division_var_right = StringVar()
divisions_list = fetch_distinct("division")
division_menu_right = OptionMenu(frm_right, division_var_right, *divisions_list) if divisions_list else OptionMenu(frm_right, division_var_right, "")
division_menu_right.place(x=20, y=270, width=160)
lbl_div = Label(frm_right, text="Division", bg="#0a3839", fg="white")
lbl_div.place(x=20, y=246)

def show_by_div_cmd():
    sel = division_var_right.get()
    if not sel:
        return
    rows = fetch_by_division(sel)
    dialog_module.displayDialog(root, rows)

btn_showdiv = Button(frm_right, text="Show By Division", bg="#ffd6a5", font=FONT_BTN, command=show_by_div_cmd)
btn_showdiv.place(x=190, y=270, width=130)

def populate_divisions():
    divs = fetch_distinct("division")
    menu = division_dropdown["menu"]
    menu.delete(0, "end")
    if divs:
        for dv in divs:
            menu.add_command(label=dv, command=lambda v=dv: division_var.set(v))
        division_var.set(divs[0])
    else:
        division_var.set("")

populate_divisions()

def on_playoff_toggle():
    team_name = entry_team.get().strip()
    if not team_name:
        return
    val = 1 if made_playoffs_var.get() else 0
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("UPDATE Teams SET playoff = ? WHERE team = ?", (val, team_name))
        con.commit()
        con.close()
    except:
        pass

def display_at(index):
    global current_index
    rows = fetch_all_teams()
    if not rows:
        clear_form()
        return
    if index < 0 or index >= len(rows):
        return
    current_index = index
    row = rows[index]
    entry_team.delete(0, END); entry_team.insert(END, row[0])
    entry_coach.delete(0, END); entry_coach.insert(END, row[1])
    entry_city.delete(0, END); entry_city.insert(END, row[2])
    entry_wins.delete(0, END); entry_wins.insert(END, str(row[3]))
    entry_losses.delete(0, END); entry_losses.insert(END, str(row[4]))
    entry_points.delete(0, END); entry_points.insert(END, str(row[5]))
    entry_avg.config(state='normal')
    entry_avg.delete(0, END)
    entry_avg.insert(END, str(row[6]))
    entry_avg.config(state='readonly')
    division_var.set(row[7] if row[7] else "")
    made_playoffs_var.set(int(row[8]) if row[8] else 0)
    text_description.delete("1.0", END)
    text_description.insert(END, row[9])

def next_entry():
    global current_index
    rows = fetch_all_teams()
    if not rows:
        return
    if current_index < len(rows) - 1:
        display_at(current_index + 1)

def prev_entry():
    global current_index
    if current_index > 0:
        display_at(current_index - 1)

def clear_form():
    entry_team.delete(0, END)
    entry_coach.delete(0, END)
    entry_city.delete(0, END)
    entry_wins.delete(0, END)
    entry_losses.delete(0, END)
    entry_points.delete(0, END)
    entry_avg.config(state='normal')
    entry_avg.delete(0, END)
    entry_avg.config(state='readonly')
    division_var.set("")
    made_playoffs_var.set(0)
    text_description.delete("1.0", END)

def insert_cmd():
    team = entry_team.get().strip()
    coach = entry_coach.get().strip()
    city = entry_city.get().strip()
    try:
        wins = int(entry_wins.get() or 0)
    except:
        messagebox.showerror("Invalid", "Wins must be an integer.")
        return
    try:
        losses = int(entry_losses.get() or 0)
    except:
        messagebox.showerror("Invalid", "Losses must be an integer.")
        return
    try:
        points = int(entry_points.get() or 0)
    except:
        messagebox.showerror("Invalid", "Points must be an integer.")
        return
    division = division_var.get()
    playoff = 1 if made_playoffs_var.get() else 0
    desc = text_description.get("1.0", END).strip()
    avg = round(points / (wins if wins>0 else 1), 2)
    if not team:
        messagebox.showwarning("Missing", "Team name is required.")
        return
    new_row = (team, coach, city, wins, losses, points, avg, division, playoff, desc)
    try:
        insert_team_to_db(new_row)
    except Exception as e:
        messagebox.showerror("Error", f"Could not insert team: {e}")
        return
    cities = fetch_distinct("city")
    menu = city_menu["menu"]
    menu.delete(0, "end")
    for c in cities:
        menu.add_command(label=c, command=lambda v=c: city_var.set(v))
    populate_divisions()
    rows = fetch_all_teams()
    display_at(len(rows) - 1)

def delete_current_team():
    team = entry_team.get().strip()
    if not team:
        messagebox.showwarning("No Team", "No team selected to delete.")
        return
    confirm = messagebox.askyesno("Confirm Delete", f"Delete team '{team}' from database?")
    if not confirm:
        return
    try:
        delete_team_in_db(team)
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed: {e}")
        return
    cities = fetch_distinct("city")
    menu = city_menu["menu"]
    menu.delete(0, "end")
    for c in cities:
        menu.add_command(label=c, command=lambda v=c: city_var.set(v))
    populate_divisions()
    rows = fetch_all_teams()
    if rows:
        display_at(0)
    else:
        clear_form()

all_rows = fetch_all_teams()
if all_rows:
    display_at(0)

btn_quit = Button(frm_right, text="Quit", bg="#ef476f", font=FONT_BTN, command=root.quit)
btn_quit.place(x=20, y=340, width=300)

root.mainloop()
