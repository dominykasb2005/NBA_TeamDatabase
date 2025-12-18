from tkinter import *

def displayDialog(parent_window, team_list):
    window = Toplevel(parent_window)
    window.title("Teams Database")
    window.geometry("1200x600")
    window.configure(bg="white")

    lbl = Label(window, text="Teams Database", font=("Helvetica", 14, "bold"), bg="white", fg="black")
    lbl.place(x=14, y=8)

    btn_close = Button(window, text="Close", command=window.destroy, font=("Helvetica", 10, "bold"))
    btn_close.place(x=1050, y=8, width=120)

    text = Text(window, undo=True, height=34, width=140, bg="white", fg="black")
    text.place(x=14, y=44)

    def display_all():
        text.delete("1.0", END)
        header = f"{'Team':36}\t{'Coach':18}\t{'City':12}\t{'W':>3}\t{'L':>3}\t{'Points':>7}\t{'Avg':>7}\t{'Division':10}\t{'Playoff':7}\t{'Arena/Description'}\n"
        text.insert(END, header)
        text.insert(END, "-" * 220 + "\n\n")
        for row in team_list:
            team = row[0]
            coach = row[1]
            city = row[2]
            wins = row[3]
            losses = row[4]
            points = row[5]
            avg = row[6]
            division = row[7] or ""
            playoff = "Yes" if row[8] else "No"
            desc = row[9] or ""
            line = f"{team:36}\t{coach:18}\t{city:12}\t{wins:>3}\t{losses:>3}\t{points:>7}\t{avg:>7}\t{division:10}\t{playoff:7}\t{desc}\n\n"
            text.insert(END, line)

    display_all()
