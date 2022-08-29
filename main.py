
import sounddevice as sd
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import tkinter as tk

# Set Wave Variables
sample_rate = 44100
amp = .1
freq = 440
x = 0
y = np.sin(2*np.pi*freq*x) * amp

def change_freq(event):
    global freq
    freq = freq_slider.get()

def change_amp(event):
    global amp
    amp = amp_slider.get()/100

    
# Wave stream callback
start_idx = 0
def callback(outdata, frames, time, status):
    global start_idx
    global x
    global y
    


    x = (start_idx + np.arange(frames))/sample_rate
    x = x.reshape(-1, 1)

    #if (current_wave.get() == "sine"):
    y = np.sin(2*np.pi*freq*x) * amp
    #elif (current_wave.get() == "tri"):
        #y = ((4*amp)/ (1/freq)) * np.absolute(np.mod((x-1), 1/freq) - (1/freq)/2) - amp

    outdata[:] = y
    

    start_idx += frames
    


# Tk Widgets
app = tk.Tk()
app.geometry("400x400")

amp_slider = tk.Scale(app, from_=1, to=100, length=300, orient=tk.HORIZONTAL, command=change_amp)
amp_slider.pack()

freq_slider = tk.Scale(app, from_=100, to=3000, length=300, orient=tk.HORIZONTAL, command=change_freq)
freq_slider.pack()

#current_wave = tk.StringVar()

#def switchWave():
#    global start_idx
#    start_idx = 0


#radio1 = tk.Radiobutton(app, text="Sine Wave", variable=current_wave, value="sine", command=switchWave)
#radio1.select()
#radio1.pack()

#radio2 = tk.Radiobutton(app, text="Triangle Wave", variable=current_wave, value="tri", command=switchWave)
#radio2.pack()


#Play Wave

stream = sd.OutputStream(
            samplerate=sample_rate, dtype="float32",
            device=sd.default.device, channels=1,
            callback=callback)

stream.start()

#Graph Stream

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def animate(i):

    a.clear()
    a.set_ylim([-1,1])
    a.set_axis_off()
    a.margins(0, 0)
    a.plot(x, y)
    
canvas = FigureCanvasTkAgg(f, app)
canvas.draw()
canvas.get_tk_widget().pack()


ani = animation.FuncAnimation(f, animate, interval=10)

#Run App
app.mainloop()

