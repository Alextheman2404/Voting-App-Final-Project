from tkinter import *
from tkinter import messagebox
import os
from data import VotingData


class Tooltip:
    """
    A class to create tooltips for widgets in a Tkinter GUI.

    Attributes:
        widget: The widget to which the tooltip is attached.
        text: The text to display in the tooltip.
        tooltip_window: The window that displays the tooltip.
    """

    def __init__(self, widget, text):
        """
        Initialize the Tooltip with a widget and text.

        :param widget: The widget to attach the tooltip to.
        :param text: The text to display in the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)

    def show_tooltip(self, event):
        """
        Display the tooltip when the mouse enters the widget.

        :param event: The event that triggered the method.
        """
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        """
        Hide the tooltip when the mouse leaves the widget.

        :param event: The event that triggered the method.
        """
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class VotingApp(Frame):
    """
    A class to represent a voting application GUI built with Tkinter.

    Attributes:
        window: The main window of the Tkinter application.
        voting_data: An instance of the VotingData class for handling voting data.
    """

    def __init__(self, window):
        """
        Initialize the VotingApp with the main window.

        :param window: The main Tkinter window.
        """
        super().__init__(window)
        self.window = window
        self.configure(bg="#f0f0f0")
        self.grid(sticky="nsew")

        # Initialize the voting data handler
        self.voting_data = VotingData()

        # Create the interface
        self.create_widgets()
        self.update_vote_tally()  # Initialize with current vote tally

        # Configure grid rows and columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def create_widgets(self):
        """
        Create and arrange the widgets for the voting application.
        """
        # Frame for the ID entry
        self.frame_id = Frame(self, bg="#f0f0f0")
        self.frame_id.grid(row=0, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
        self.label_id = Label(self.frame_id, text='Unique ID:', width=15, bg="#f0f0f0", font=("Arial", 12))
        self.label_id.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.input_id = Entry(self.frame_id, width=30, font=("Arial", 12))
        self.input_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        Tooltip(self.label_id, "Enter a unique numeric ID.")

        # Frame for the voting options
        self.frame_vote = Frame(self, bg="#f0f0f0")
        self.frame_vote.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
        self.vote_var = StringVar(None, "A")
        self.vote_label = Label(self.frame_vote, text="Vote:", width=15, bg="#f0f0f0", font=("Arial", 12))
        self.vote_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.option_john_radio = Radiobutton(self.frame_vote, text="John", variable=self.vote_var, value="John",
                                             bg="#f0f0f0", font=("Arial", 12))
        self.option_jane_radio = Radiobutton(self.frame_vote, text="Jane", variable=self.vote_var, value="Jane",
                                             bg="#f0f0f0", font=("Arial", 12))
        self.option_john_radio.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.option_jane_radio.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        Tooltip(self.option_john_radio, "Select this option to vote for John.")
        Tooltip(self.option_jane_radio, "Select this option to vote for Jane.")

        # Frame for the submit button
        self.frame_save = Frame(self, bg="#f0f0f0")
        self.frame_save.grid(row=2, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
        self.save_button = Button(self.frame_save, text='Submit Vote', command=self.confirm_vote, bg="#4CAF50",
                                  fg="white", font=("Arial", 12))
        self.save_button.pack(side=TOP, padx=5, pady=5)

        # Status message
        self.error_message = Label(self.frame_save, text="", fg="red", bg="#f0f0f0", font=("Arial", 12))
        self.error_message.pack(side=TOP, padx=5, pady=5)

        # Frame for vote tally
        self.frame_tally = Frame(self, bg="#f0f0f0")
        self.frame_tally.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky="ew")
        self.tally_label = Label(self.frame_tally, text="Current Tally:", width=15, bg="#f0f0f0", font=("Arial", 12))
        self.tally_display = Label(self.frame_tally, text="", bg="#f0f0f0", font=("Arial", 12))
        self.tally_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.tally_display.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    def update_vote_tally(self):
        """
        Update the vote tally display in the GUI.
        """
        tally = self.voting_data.get_vote_tally()
        tally_text = f"John: {tally['John']}   Jane: {tally['Jane']}"
        self.tally_display.config(text=tally_text)
    def confirm_vote(self):
        """
        Display a confirmation dialog before submitting the vote.
        """
        if messagebox.askyesno("Confirm Vote", "Are you sure you want to submit this vote?"):
            self.submit_vote()

    def submit_vote(self):
        """
        Submit the vote after validating the unique ID and selected vote option.
        """
        unique_id = self.input_id.get().strip()
        vote = self.vote_var.get()

        # Validate the unique identifier
        if not unique_id:
            self.error_message.config(text="ID cannot be empty", fg="red")
            return
        if not unique_id.isdigit():
            self.error_message.config(text="ID can only contain numbers", fg="red")
            return

        # Validate the vote selection
        if not vote:
            self.error_message.config(text="Please pick a vote", fg="red")
            return

        # Check if ID is unique
        if not self.voting_data.validate_id(unique_id):
            self.error_message.config(text="ID already used", fg="red")
            return

        # Record the vote
        try:
            if vote == "A":
                self.error_message.config(text="Please pick a vote first", fg="red")
            else:
                self.voting_data.record_vote(unique_id, vote)
                self.error_message.config(text="Vote recorded successfully!", fg="green")
                self.update_vote_tally()
        except Exception as e:
            self.error_message.config(text="Error recording vote", fg="red")
