from tkinter import *
import requests
import random


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Tester")
        self.resizable(width=True, height=True)
        self.config(padx=50, pady=50, bg="#34b4eb")
        self.geometry("+%d+%d" % (self.winfo_screenwidth()*0.20, self.winfo_screenheight()*0.25))

        self.rcpm = 0
        self.ccpm = 0
        self.wpm = 0
        self.word = ""

        rcpm_label = Label(self, text="rCPM", font=("Arial", 15), bg="#34b4eb")
        rcpm_label.grid(row=0, column=0, padx=20, pady=5)
        self.rcpm_count = Label(self, text=self.rcpm, font=("Arial", 12), bg="#34b4eb")
        self.rcpm_count.grid(row=1, column=0, padx=20, pady=5)

        ccpm_label = Label(self, text="cCPM", font=("Arial", 15), bg="#34b4eb")
        ccpm_label.grid(row=0, column=1, padx=20, pady=5)
        self.ccpm_count = Label(self, text=self.ccpm, font=("Arial", 12), bg="#34b4eb")
        self.ccpm_count.grid(row=1, column=1, padx=20, pady=5)

        wpm_label = Label(self, text="WPM", font=("Arial", 15), bg="#34b4eb")
        wpm_label.grid(row=0, column=2, padx=20, pady=5)
        self.wpm_count = Label(self, text=self.wpm, font=("Arial", 12), bg="#34b4eb")
        self.wpm_count.grid(row=1, column=2, padx=20, pady=5)

        self.start = Button(self, text="Start", command=self.start_test)
        self.start.grid(column=0, row=2, columnspan=3, rowspan=2, padx=20, pady=5)


        self.info = Text(self, height=6, width=53)
        self.info.insert(END, "CPM and WPM: They're short for Characters Per Minute,and Words Per Minute. The "
                              "'raw CPM' (rCPM) is the    actual number of characters you type per minute,     including "
                              "all the mistakes. 'Corrected' (cCPM) scorescount only correctly typed words. "
                              "'WPM' is just the  corrected CPM divided by 5.")
        self.info.grid(column=0, row=4, columnspan=3, padx=20, pady=5)

        with open("scores.txt", "r") as score:
            # Update high score
            hs = score.read()
            self.high_score = Label(self, text=f"WPM High Score: {hs}", font=("Arial", 15), bg="#34b4eb")
            self.high_score.grid(column=0, row=5, columnspan=3, padx=20, pady=5)

        self.bind("<Return>", lambda event: self.word_entry())

    def start_test(self):
        self.start.destroy()

        self.word_label = Label(self, text=self.word, font=("Arial", 14), bg="#34b4eb")
        self.word_label.grid(column=0, row=2, columnspan=3, padx=20, pady=5)

        self.entry = Entry(self)
        self.entry.grid(column=0, row=3, columnspan=3, padx=20, pady=10)

        self.random_word()

        timer = Timer()
        if timer:
            self.after(60000, self.end_test)

    def random_word(self):
        with open("words.txt", "r") as word_list:
            words = word_list.readlines()
            self.word = random.choice(words)
            self.word_label.config(text=self.word.lower())

    def word_entry(self):
        typed_entry = self.entry.get()
        self.typed_entry = list(typed_entry+"\n")
        self.word = list(self.word)
        self.calc_stats()
        self.entry.delete(0, END)
        self.random_word()

    def calc_stats(self):
        # Calculate cCPM
        if self.typed_entry == self.word:
            self.ccpm += len(self.word)

        self.ccpm_count.config(text=self.ccpm)

        # Calculate rCPM
        entry_length = len(self.typed_entry)
        self.rcpm += entry_length - 1
        self.rcpm_count.config(text=self.rcpm)

        # Add to WPM
        self.wpm = self.ccpm / 5
        self.wpm_count.config(text=self.wpm)

    def end_test(self):
        self.entry.destroy()
        self.word_label.destroy()
        self.scoreboard()
        self.restart = Button(self, text="Restart", command=self.restart_test)
        self.restart.grid(column=0, row=2, columnspan=3, rowspan=2, padx=20, pady=5)

    def scoreboard(self):
        with open("scores.txt", "r") as score:
            high_score = score.read()
            if self.wpm > float(high_score):
                self.update_score()

    def update_score(self):
        with open("scores.txt", "w") as score:
            score.write(f"{self.wpm}")
            self.high_score.config(text=f"WPM High Score: {self.wpm}")

    def restart_test(self):
        self.rcpm = 0
        self.ccpm = 0
        self.wpm = 0
        self.restart.destroy()
        self.rcpm_count.config(text=self.rcpm)
        self.ccpm_count.config(text=self.ccpm)
        self.wpm_count.config(text=self.wpm)
        self.start_test()


class Timer(Tk):
    def __init__(self):
        super().__init__()
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        self.title("Timer")
        self.resizable(width=True, height=True)
        self.config(padx=50, pady=50)
        self.geometry("+%d+%d" % (ws*0.50, hs*0.25))

        self.start_time = 60

        self.timer = Label(self, text=self.start_time, font=("Arial", 15))
        self.timer.grid(column=0, row=0)
        self.sec = Label(self, text="sec", font=("Arial", 15))
        self.sec.grid(column=1, row=0)

        self.count_down(count=self.start_time)

    def count_down(self, count):
        if count > 0:
            self.start_time = self.after(1000, self.count_down, count-1)
            self.timer.config(text=count)
        else:
            self.destroy()


def word_generator():
    with open("words.txt", "a") as word_list:
        for num in range(100):
            response = requests.get("https://api.api-ninjas.com/v1/randomword", headers={"X-Api-Key": "7GhzLS5vITfbGRXs3TMo+Q==omGai7Kl3XSwovoT"}, params={"type": "verb"})
            # Type of words able to request (optional): noun, verb, adjective, adverb
            if response.status_code == requests.codes.ok:
                word = response.json()["word"]
                word_list.write(f"{word}\n")
            else:
                print("Error:", response.status_code, response.text)


# Run if new words are needed
# word_generator()

root = App()
root.mainloop()
