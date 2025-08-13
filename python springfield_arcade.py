import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# --- Classes ---
class SlotMachine:
    def __init__(self, location_name):
        self.symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
        self.location_name = location_name

    def spin(self):
        return [random.choice(self.symbols) for _ in range(3)]

class Minion:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.unlocked_minions = []
        self.current_location = None

    def smart_play(self, machine):
        result = machine.spin()
        display = " | ".join(result)
        bonus = 0

        counts = {s: result.count(s) for s in result}
        for symbol, count in counts.items():
            if count == 3:
                bonus = 10
                self.unlock_minion(symbol)
                break
            elif count == 2:
                bonus = 3

        self.points += bonus
        return display, bonus

    def unlock_minion(self, symbol):
        minion_name = f"Mini_{symbol}"
        if minion_name not in self.unlocked_minions:
            self.unlocked_minions.append(minion_name)
            print(f"Unlocked new minion: {minion_name}!")

class Environment:
    def __init__(self):
        self.nearby_characters = []

    def is_phineas_near(self):
        return "Phineas" in self.nearby_characters

# --- GUI ---
class SpringfieldArcade(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Springfield Slot Arcade - Ultimate Upgraded")
        self.geometry("800x600")

        self.locations = ["North Glenstone", "Shell", "Phillips 66", "VP", "White Oak", "Other"]
        self.machines = {loc: SlotMachine(loc) for loc in self.locations}
        self.minions = [Minion("MiniBot1"), Minion("MiniBot2")]
        self.env = Environment()

        self.create_widgets()
        self.automate_minions()

    def create_widgets(self):
        self.info_label = tk.Label(self, text="Springfield Slot Arcade", font=("Arial", 16))
        self.info_label.pack(pady=10)

        # Location buttons
        self.location_frame = tk.Frame(self)
        self.location_frame.pack(pady=5)

        for loc in self.locations:
            btn = tk.Button(self.location_frame, text=loc, command=lambda l=loc: self.select_location(l))
            btn.pack(side=tk.LEFT, padx=5)

        # Phineas toggle
        self.phineas_button = tk.Button(self, text="Toggle Phineas Presence", command=self.toggle_phineas)
        self.phineas_button.pack(pady=5)

        # Display results
        self.result_text = tk.Text(self, height=15, width=90)
        self.result_text.pack(pady=10)

        self.score_label = tk.Label(self, text="", font=("Arial", 12))
        self.score_label.pack(pady=5)

    def select_location(self, location):
        for minion in self.minions:
            minion.current_location = location
        self.result_text.insert(tk.END, f"Minions moved to {location}\n")
        self.result_text.see(tk.END)

    def smart_spin(self, minion):
        if self.env.is_phineas_near() and minion.current_location:
            machine = self.machines[minion.current_location]
            display, bonus = minion.smart_play(machine)
            self.result_text.insert(tk.END, f"{minion.name} spun at {minion.current_location}: {display}\n")
            if bonus >= 10:
                self.result_text.insert(tk.END, f"*** {minion.name} HIT JACKPOT! Unlocked new minion! ***\n")
                messagebox.showinfo("Jackpot!", f"{minion.name} hit the jackpot at {minion.current_location}!")
            self.result_text.see(tk.END)

    def toggle_phineas(self):
        if "Phineas" in self.env.nearby_characters:
            self.env.nearby_characters.remove("Phineas")
        else:
            self.env.nearby_characters.append("Phineas")
        status = "near" if self.env.is_phineas_near() else "far"
        self.info_label.config(text=f"Phineas is {status}.")

    def automate_minions(self):
        def run():
            while True:
                for minion in self.minions:
                    # If no location set, pick random
                    if not minion.current_location:
                        minion.current_location = random.choice(self.locations)
                    self.smart_spin(minion)
                self.update_scores()
                time.sleep(5)  # spin every 5 seconds
        t = threading.Thread(target=run, daemon=True)
        t.start()

    def update_scores(self):
        score_text = ""
        for minion in self.minions:
            score_text += f"{minion.name} Points: {minion.points}, Unlocked: {', '.join(minion.unlocked_minions) if minion.unlocked_minions else 'None'}\n"
        self.score_label.config(text=score_text)

# --- Run App ---
if __name__ == "__main__":
    app = SpringfieldArcade()
    app.mainloop()
