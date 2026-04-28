import tkinter as tk
import random
import time
from tkinter import messagebox

class MainGUI:
    def __init__(self):

        ##self.hostbal = 50000000

        self.CurrentV = 500000000

        self.wagerV = 0

        self.currentB = 0

        self.currentR = 0

        self.diceX = 0.5

        self.amountbet = 0

        self.diceval = 0.006

        self.profit = 0

        self.amountbetx2 = 0

        self.root = tk.Tk()
        self.root.geometry("1280x820")
        self.root.title("RippleRL")

        self.dice_photo = tk.PhotoImage(file="dice.png")
        self.straw_photo = tk.PhotoImage(file="straw.png")
        self.bg_photo = tk.PhotoImage(file="bg.png")

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.straw_label = tk.Label(self.root, image=self.straw_photo)
        self.straw_label.place(relx=0.5, rely=0.6, anchor="center")

        self.image_label = tk.Label(self.root, image=self.dice_photo)
        self.image_label.place(relx=self.diceX, rely=0.6, anchor="center")


        self.button = tk.Button(
            self.root,
            text="ROLL",
            font=('Arial', 18),
            height=3,
            width=15,
            command=self.roll
        )

        self.button.place(relx=0.5, rely=0.1, anchor="center")

        buttonframe = tk.Text(self.root, height=12, font=('Arial, 26'))
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)

        btn1 = tk.Button(buttonframe, text="All in", font=('Arial, 18'), command=self.gm1)
        btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

        btn2 = tk.Button(buttonframe, text="5k", font=('Arial, 18'), command=self.gm2)
        btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

        btn3 = tk.Button(buttonframe, text="10k", font=('Arial, 18'), command=self.gm3)
        btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

        btn4 = tk.Button(buttonframe, text="20k", font=('Arial, 18'), command=self.gm4)
        btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

        btn5 = tk.Button(buttonframe, text="50k", font=('Arial, 18'), command=self.gm5)
        btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

        btn6 = tk.Button(buttonframe, text="100k", font=('Arial, 18'), command=self.gm6)
        btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

        buttonframe.place(relx=0.5, rely=0.8, anchor="center")

        self.check_state = tk.IntVar()

        autocheck = tk.Checkbutton(
        self.root,
        text="auto",
        font=("Arial", 18),
        variable=self.check_state
)
        autocheck.place(relx=0.1, rely=0.6, anchor="center")

        self.displayV = tk.Label(self.root, font=('Arial', 28))
        self.displayV.place(relx=0.9, rely=0.1, anchor="center")

        self.rbval = tk.Label(self.root, font=('Arial', 28))
        self.rbval.place(relx=0.1, rely=0.1, anchor="center")

        self.protittag = tk.Label(self.root, font=('Arial', 22))
        self.protittag.place(relx=0.5, rely=0.35, anchor="center")

        self.displayRolledV = tk.Label(self.root, font=('Arial', 28))
        self.displayRolledV.place(relx=0.5, rely=0.4, anchor="center")

        self.textbox = tk.Text(self.root, height=2, width=10, font=('Arial', 17))
        self.textbox.bind("<Control-Return>", self.setbet)
        self.textbox.place(relx=0.5, rely=0.9, anchor="center")

        self.displayV.config(text=self.CurrentV)

        self.root.mainloop()

    def roll(self):
        if self.amountbet == 0:
            messagebox.showinfo(title="Error 212", message="Invalid Amount Bet (Error:2, Invalid Amount Bet.)")
        else:
            if self.currentB == 0:
                if self.CurrentV >= self.amountbet:
                    self.currentB = 1
                    self.wagerV += 0.0001 * self.amountbet
                    self.CurrentV -= self.amountbet
                    self.currentR = random.randint(1, 3)
                    if self.currentR <= 2:
                        premrolledV = random.randint(1,self.amountbet)
                    else:
                        premrolledV = random.randint(self.amountbet, self.amountbetx2)

                    RolledV = premrolledV
                    self.diceX = 0.2 + RolledV * self.diceval
                    self.image_label.place(relx=self.diceX, rely=0.6, anchor="center")
                    self.displayRolledV.config(text=RolledV)
                    self.protittag.config(text=RolledV-self.amountbet)
                    print(RolledV)
                    self.CurrentV += RolledV
                    print(self.CurrentV)
                    print(self.wagerV)
                    self.displayV.config(text=self.CurrentV)
                    self.root.after(700, self.reset_roll)
                else:
                    messagebox.showinfo(title="Error 34", message="Not enough balance. (Error:34, Not enough balance.)")
            else:
                messagebox.showinfo(title="Error 212", message="Cooldown 0.7. (Error:18, if after 0.7 seconds cooldown not gone restart launcher.)")
    
    def reset_roll(self):
        self.currentB = 0
        if self.check_state.get() == 1:
            self.roll()

    def gm1(self):
        self.amountbet = self.CurrentV
        self.amountbetx2 = self.CurrentV * 2
        self.diceval = 0.3 / self.amountbet
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)
        
    def gm2(self):
        self.amountbet = 5000
        self.amountbetx2 = 10000
        self.diceval = 0.00006
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)

    def gm3(self):
        self.amountbet = 10000
        self.amountbetx2 = 20000
        self.diceval = 0.00003
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)

    def gm4(self):
        self.amountbet = 20000
        self.amountbetx2 = 40000
        self.diceval = 0.000015
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)
        
    def gm5(self):
        self.amountbet = 50000
        self.amountbetx2 = 100000
        self.diceval = 0.000006
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)

    def gm6(self):
        self.amountbet = 100000
        self.amountbetx2 = 200000
        self.diceval = 0.000003
        self.profit = self.amountbet
        self.rbval.config(text=self.amountbet)


    def setbet(self, event=None):
        try:
            value = int(self.textbox.get("1.0", tk.END).strip())

            self.amountbet = value
            self.amountbetx2 = value * 2
            self.diceval = 0.6 / self.amountbetx2

            self.rbval.config(text=self.amountbet)

        except ValueError:
            messagebox.showinfo(
                title="Error 212",
                message='Invalid String Sequence (Error 42: Type only numbers. "k, m, b" not supported.)'
            )


MainGUI()