import tkinter as tk
import random
import time
from tkinter import messagebox
import flask
from flask import Flask, request, jsonify


app = Flask(__name__)



class BK:
    def __init__(self):

        self.CurrentV = 500000000
        self.wagerV = 0
        self.currentB = 0
        self.currentR = 0
        self.diceX = 0.5
        self.amountbet = 0
        self.diceval = 0.006
        self.profit = 0
        self.amountbetx2 = 0

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
                    print(RolledV)
                    self.CurrentV += RolledV
                    print(self.CurrentV)
                    print(self.wagerV)
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

    #def setbet(self, event=None):
        #try:

            #self.amountbet = value
            #self.amountbetx2 = value * 2
            #self.diceval = 0.6 / self.amountbetx2

        #except ValueError:
            #messagebox.showinfo(title="Error 212", message='Invalid String Sequence (Error 42: Type only numbers. "k, m, b" not supported.)')


BK()

@app.route("/api/roll", methods=["POST"])
def api_roll():
    # For demo: just return a random number as the roll result
    result = random.randint(1, 100)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)