"""
Written by: Matthew Chang

visualization tool for circular convolution

Source for Embedding Live Matplotlib graphs:
https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
https://pythonprogramming.net/python-matplotlib-live-updating-graphs/
"""

import math
import matplotlib
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import time
from tkinter import Tk, Canvas, Label, Entry, Button, ALL
from tkinter import messagebox


matplotlib.use("TkAgg")
style.use('ggplot')  # use ggplot style
DELAY = 0.03  # canvas refresh rate
ROTATE_RATE = 3  # how fast bubbles rotate (in degrees per refresh)
DPI = 100


class CircularConv:
    def __init__(self, size):
        if not 300 <= size <= 750:
            raise ValueError('The size of the window is unreasonable')
        self.root = Tk()
        self.root.title('Circular Convolution Visualizer')
        self.size = size
        self.signal1 = []
        self.signal2 = []
        self.result = []
        self.angle = 0
        self.spacing = 0
        self.count = 0
        self.prevCount = -1

        # scale the elements based on input size
        self.center = self.size / 2
        self.innerRadius = self.size * 3/10
        self.outerRadius = self.size * 2/5
        self.innerBound1 = self.size/5
        self.innerBound2 = self.size * 4/5
        self.outerBound1 = self.size/10
        self.outerBound2 = self.size * 9/10
        self.bubbleBound = self.size * 3/100
        self.fontSize = str(int(self.size * 12/500))
        self.figSize = int(self.size // 120)

        # define the widgets
        self.canvas = Canvas(self.root, width=self.size, height=self.size, bg='white')
        self.label1 = Label(self.root, text='First Signal')
        self.entry1 = Entry(self.root)
        self.label2 = Label(self.root, text='Second Signal')
        self.entry2 = Entry(self.root)
        self.label3 = Label(self.root, text='Number of Padded Zeros')
        self.entry3 = Entry(self.root)
        self.button1 = Button(self.root, text='Convolute', command=self.addSignal)
        self.button2 = Button(self.root, text='Reset', command=self.reset)
        self.button3 = Button(self.root, text='Step', command=self.nextStep)
        self.fig = Figure(figsize=(self.figSize, self.figSize), dpi=DPI)
        self.graph = FigureCanvasTkAgg(self.fig, self.root)

        # add plot
        self.plt = self.fig.add_subplot(111)
        self.plt.set_xlabel('Time, samples')
        self.plt.set_ylabel('CC output')
        self.graph.draw()

        # position widgets in layout
        self.canvas.grid(row=0, column=0, rowspan=20)
        self.label1.grid(row=1, column=1)
        self.entry1.grid(row=2, column=1)
        self.label2.grid(row=3, column=1)
        self.entry2.grid(row=4, column=1)
        self.label3.grid(row=5, column=1)
        self.entry3.grid(row=6, column=1)
        self.button1.grid(row=7, column=1)
        self.button2.grid(row=8, column=1)
        self.button3.grid(row=11, column=1)
        self.graph.get_tk_widget().grid(row=0, column=2, rowspan=20)

    # adds signals to the canvas
    def addSignal(self):
        if not self.entry1.get() or not self.entry2.get():
            # note: this method doesn't return till the messagebox is closed
            messagebox.showerror('Error', 'Please input both signals!')
            return

        self.reset()  # clear everything

        # get signal from entries
        self.signal1 = self.entry1.get().split(',')
        self.signal2 = self.entry2.get().split(',')

        if len(self.signal1) != len(self.signal2):
            self.signal1 = []
            self.signal2 = []
            messagebox.showerror('Error',
                                 'Make sure the signals have the same length!')
            return

        # pad the zeros
        numZeros = int(self.entry3.get()) if self.entry3.get() else 0
        self.signal1.extend(['0'] * numZeros)
        self.signal2.extend(['0'] * numZeros)

        # angle between bubbles
        self.spacing = 360 / len(self.signal1)

        # make signals into lists of list of Cartesian coordinates and the data
        for i in range(len(self.signal1)):
            x, y = self.getCartesian(self.outerRadius, -i*self.spacing)
            self.signal1[i] = [x, y, self.signal1[i]]
            x, y = self.getCartesian(self.innerRadius, i*self.spacing)
            self.signal2[i] = [x, y, self.signal2[i]]

        self.canvas.delete(ALL)
        self.drawShapes()

    # clear and reset the canvas
    def reset(self):
        self.canvas.delete(ALL)
        self.canvas.update()
        self.signal1 = []
        self.signal2 = []
        self.result = []
        self.angle = 0
        self.spacing = 0
        self.count = 0
        self.prevCount = -1
        self.plt.clear()

    # go onto the next step in circular convolution
    def nextStep(self):
        if len(self.signal1) != 0:
            self.rotateBubble(-self.spacing)
            self.count += 1

    # updates the plot
    def animate(self, i):
        length = len(self.signal1)
        # update plot only when you go to the next step
        if self.prevCount != self.count and length > 0:
            tmp = 0
            # compute circular convolution
            for j in range(len(self.signal1)):
                tmp += int(self.signal1[j][2])*int(self.signal2[(self.count-j) % length][2])
            self.result.append(tmp)
            self.plt.clear()
            self.plt.stem(range(len(self.result)), self.result)
            # use integer ticks
            ax = self.fig.gca()
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.prevCount = self.count

    # rotates the bubbles by a certain angle
    def rotateBubble(self, angle):
        step = -ROTATE_RATE if angle <= 0 else ROTATE_RATE
        finalAngle = self.angle + angle

        while abs(self.angle) < abs(finalAngle):
            for j in range(len(self.signal2)):
                self.signal2[j][0], self.signal2[j][1] = \
                    self.getCartesian(self.innerRadius, self.spacing*j + self.angle)

            self.updateCanvas()
            self.angle += step

        # ensure bubbles reach the final angle (no round-off errors)
        self.angle = finalAngle
        for j in range(len(self.signal2)):
            self.signal2[j][0], self.signal2[j][1] = \
                self.getCartesian(self.innerRadius, self.spacing*j + self.angle)

        self.updateCanvas()

    # convert polar coordinates to Cartesian
    def getCartesian(self, radius, angle):
        return self.center + radius * math.cos(angle * math.pi / 180), \
               self.center + radius * math.sin(angle * math.pi / 180)

    # draws the shapes on the canvas
    def drawShapes(self):
        # inner circle
        self.canvas.create_oval(self.innerBound1, self.innerBound1,
                                self.innerBound2, self.innerBound2,
                                outline='red')
        # outer circle
        self.canvas.create_oval(self.outerBound1, self.outerBound1,
                                self.outerBound2, self.outerBound2,
                                outline='blue')
        # bubbles of points in signal1
        for x, y, num in self.signal1:
            self.canvas.create_oval(x - self.bubbleBound, y - self.bubbleBound,
                                    x + self.bubbleBound, y + self.bubbleBound,
                                    fill='white')
            self.canvas.create_text(x, y, font=('Times', self.fontSize),
                                    text=num)
        # bubbles of points in signal2
        for x, y, num in self.signal2:
            self.canvas.create_oval(x - self.bubbleBound, y - self.bubbleBound,
                                    x + self.bubbleBound, y + self.bubbleBound,
                                    fill='white')
            self.canvas.create_text(x, y, font=('Times', self.fontSize),
                                    text=num)

    # refreshes the canvas
    def updateCanvas(self):
        self.canvas.delete(ALL)
        self.drawShapes()
        self.canvas.update()
        time.sleep(DELAY)

    # keep the window open
    def run(self):
        a = animation.FuncAnimation(self.fig, self.animate)
        self.root.mainloop()


if __name__ == '__main__':
    c = CircularConv(600)
    c.run()
