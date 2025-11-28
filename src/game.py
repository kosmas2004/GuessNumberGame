from ui import GuessNumberUi,OkMessage
import random
import customtkinter as ctk
class GuessNumberGame:

    def __init__(self, ui):
        self.ui = ui
        self.secret = random.randint(1, 100)
        self.chance = 20
        self.difficulty = "Easy"
        self.ui.guess_btn.configure(command=self.check_guess)
        self.ui.newgame_btn.configure(command=self.new_game)
        self.ui.exit_btn.configure(command=self.exit_app)
        self.ui.difficulty_segment.configure(command=self.on_difficulty_change)
        self.ui.btn_dark.configure(command=lambda: self.change_theme("Dark"))
        self.ui.btn_light.configure(command=lambda: self.change_theme("Light"))
        self.ui.hint_var.trace_add("write", self.toggle_hint)

    def check_guess(self):
        try:
            guess = int(self.ui.guess_entry.get())
        except ValueError:
            OkMessage(self.ui, "Error", f"Enter a Number")
            return
        self.chance -= 1
        self.ui.count_label.configure(text=f"You Have {self.chance} Chance To Guess")

        if guess == self.secret:
            OkMessage(self.ui, "Win", f"Congratulations, You Won!")
            self.ui.guess_btn.configure(state="disabled")
        elif guess < self.secret:
            self.ui.hint_label.configure(text="Higher!")
        elif guess > self.secret:
            self.ui.hint_label.configure(text="Lower!")

        if self.chance <= 0:
            self.ui.count_label.configure(text=f"Game Over!\nNumber was {self.secret}")
            self.ui.guess_btn.configure(state="disabled")
            self.ui.hint_label.pack_forget()

    def new_game(self):
        current_difficulty = self.ui.difficulty_var.get()
        if current_difficulty == "Easy":
            self.chance = 20
        elif current_difficulty == "Normal":
            self.chance = 15
        elif current_difficulty == "Hard":
            self.chance = 10

        self.secret = random.randint(1, 100)
        self.ui.guess_entry.delete(0, "end")
        self.ui.guess_btn.configure(state="normal")
        self.ui.count_label.configure(text=f"You Have {self.chance} Chance To Guess")
        OkMessage(self.ui, "New", "New game started \n Guess Number Changed")
        self.update_hint_display()

    def on_difficulty_change(self, value):
        self.difficulty = value
        if self.difficulty == "Easy":
            self.chance = 20
        elif self.difficulty == "Normal":
            self.chance = 15
        elif self.difficulty == "Hard":
            self.chance = 7
        self.secret = random.randint(1, 100)
        self.ui.guess_entry.delete(0, "end")
        self.ui.guess_btn.configure(state="normal")
        self.ui.count_label.configure(text=f"You Have {self.chance} Chance To Guess")
        OkMessage(self.ui, "Ok", f"Difficulty set to {value}")
        self.update_hint_display()

    def update_hint_display(self):
        if self.ui.hint_var.get() == "on":
            if not self.ui.hint_label.winfo_ismapped():
                self.ui.hint_label.pack(before=self.ui.frame_btn_game)
                OkMessage(self.ui, "Hint", "Hint is On")
        else:
            if self.ui.hint_label.winfo_ismapped():
                self.ui.hint_label.pack_forget()
                OkMessage(self.ui, "Hint", "Hint is Off")

    def toggle_hint(self, *args):
        self.update_hint_display()

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)

    def exit_app(self):
        self.ui.destroy()
if __name__ == '__main__':
    ui = GuessNumberUi()
    game = GuessNumberGame(ui)
    ui.mainloop()
