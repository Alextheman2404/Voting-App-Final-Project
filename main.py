from tkinter import *
from gui import VotingApp


def main():
    window = Tk()
    window.title("Voting App")
    window.geometry("600x300")
    window.resizable(False, False)

    app = VotingApp(window)
    app.pack()

    window.mainloop()


if __name__ == "__main__":
    main()