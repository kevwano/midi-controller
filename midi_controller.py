#py 3.11
from multiprocessing.connection import Listener
import mido
import keyboard
from pynput import mouse
import time
from tkinter import *

print("Available MIDI output ports:")
for port in mido.get_output_names():
    print(port)

port_name = "loopMIDI Port 1"

outport = mido.open_output(port_name)


# Map QWERTY keys to MIDI notes
key_map = {
    "z": 60,  # C
    "s": 61,
    "x": 62,
    "d": 63,
    "c": 64,
    "v": 65,
    "g": 66,
    "b": 67,
    "h": 68,
    "n": 69,
    "j": 70,
    "m": 71,
    ",": 72,  # C
    "l": 73,
    ".": 74,
    ";": 75,
    "/": 76,
    "q":77,
    "2":78,
    "w":79,
    "3":80,
    "e":81,
    "4":82,
    "r":83,
    "t":84,
    "6":85,
    "y":86,
    "7":87,
    "u":88,
    "i":89,
    "9":90,
    "o":91,
    "0":92,
    "p":93,
    "-":94,
    "[":95
}
#setup initial program conditions
recording=False
octave=-1 #bottom note C3
key_hook=None #not taking keypresses

# Keep track of held keys to send note_off
held_keys = []

#set up window elements
root=Tk()
root.title("FREEMIDI4U!!")
root.geometry("600x300")
root.configure(bg="gray")
root.attributes('-topmost', True)

amirecording=Label(root, text="Keyboard MIDI input: OFF")
amirecording.pack()

whatoctave=Label(root, text=f"(Bottom note) Octave: C{4+octave}")
whatoctave.pack()

frame = Frame(root)
frame.place(x=25, y=100)
frame.configure(bg="gray")
    

#list of gui buttons corresponding to key notes
keys=[]
#list of labels for said buttons
labels=["z","x","c","v","b","n","m",",",".","/","s","d","g","h","j","l",";","q","w","e","r","t","y","u","i","o","p","[","2","3","4","6","7","9","0","-"]


velocity=64

def key_event(event):
    global recording
    global keys
    key = event.name
    if key in key_map and recording==True:
        note = key_map[key]+octave*12

        if(event.event_type == "down" and key not in held_keys):
            msg = mido.Message('note_on', note=note, velocity=velocity, channel=0)
            outport.send(msg)
            held_keys.append(key)
            print("playing", note)
            keys[labels.index(key)].config(relief=SUNKEN)
        elif(event.event_type == "up"):
            msg = mido.Message('note_off', note=note, velocity=velocity, channel=0)
            outport.send(msg)
            print("released", note)
            if(len(held_keys)>0):
                held_keys.remove(key)
                keys[labels.index(key)].config(relief=RAISED)
        
    if key=="esc":
        stop_recording()
    if key=="left" and event.event_type=="up":
        down_octave()
    if key=="right" and event.event_type=="up":
        up_octave()
    
    
    
keys_down=2
def start_recording(event):
    global recording
    global amirecording
    global keys_down
    global listener
    
    #  https://pynput.readthedocs.io/en/latest/mouse.html
    listener=mouse.Listener(on_scroll=on_scroll)

    #start recording shortcut detection because keyboard module hooks didn't work
    if( (event.name=='shift' or event.name=='r' or event.name=="R") and event.event_type=="down"):
        keys_down=2
        print("shortcut down")

    if ( 
        (event.name=='shift' or event.name=='r' or event.name=="R") and event.event_type=="up"
        and keys_down>0
        ):
        keys_down-=1
        print("key up", keys_down)
        if(keys_down==0):
            recording=True
            keyboard.hook(key_event, suppress=True)
            print('start recording')
            amirecording.config(text="Keyboard MIDI input: ON")
            listener.start()

def stop_recording():
    global recording
    global keys_down
    global listener
    if recording==True:
        print("Stop recording")
        recording=False
        amirecording.config(text="Keyboard MIDI input: OFF")
        keyboard.unhook(key_event)
        keys_down=2
        listener.stop()
        
def up_octave():
    global octave
    global whatoctave
    if(not octave==2):
        octave+=1
        print("+octave")
        whatoctave.config(text=f"(Bottom note) Octave: C{4+octave}")

def down_octave():
    global octave
    global whatoctave
    if(not octave==-5):
        octave-=1
        print("-octave")
        whatoctave.config(text=f"(Bottom note) Octave: C{4+octave}")


def modwheelinput(value):
    msg = mido.Message('control_change', control=int(value), channel=0)
    outport.send(msg)
    print("modwheel update", value)

def velocitychange(value):
    global velocity
    velocity=int(value)
    print("velocity change", value)

#0 is velocity, 1 is modwheel
currentwheelcontrol=IntVar(value=0)

def on_scroll(x, y, dx, dy):
    global currentwheelcontrol
    control=currentwheelcontrol.get()
    global velocitywheel
    global modwheel
    print("scrolling", dy)
    if control==0:
        velocitywheel.set(velocitywheel.get()+dy*5)
    elif control==1:
        modwheel.set(modwheel.get()+dy*5)

def main():

    for i in range(10):
        btn = Button(frame,text=labels[i],command="",width=4,height=2)
        btn.grid(column=2*i, columnspan=2,row=4)
        keys.append(btn)

    a=0
    for i in range(7):
        btn = Button(frame,text=labels[i+10],command="",width=4,height=2, bg="black", fg="white")
        if i in [2, 5]:
            a+=2
        btn.grid(column=2*i+1+a, columnspan=2,row=3)
        keys.append(btn)

    for i in range(11):
        btn = Button(frame,text=labels[i+17],command="",width=4,height=2)
        btn.grid(column=2*i, columnspan=2, row=2)
        keys.append(btn)
    
    a=0
    for i in range(8):
        btn = Button(frame,text=labels[i+28],command="",width=4,height=2, bg="black", fg="white")
        if i in [3,5]:
            a+=2
        btn.grid(column=2*i+1+a, columnspan=2,row=1)
        keys.append(btn)
    
    keyboard.hook(start_recording)

    global modwheel
    modwheel=Scale(frame, from_=0, to=127, orient="vertical", command=modwheelinput, label="mod")
    modwheel.set(0)
    modwheel.grid(column=27, row=2, rowspan=5)

    global velocitywheel
    velocitywheel=Scale(frame, from_=0, to=127, orient="vertical", command=velocitychange, label="vel")
    velocitywheel.set(64)
    velocitywheel.grid(column=25, row=2, rowspan=5)
    
    global wheelswitch
    wheelswitch=Scale(frame, from_=0, to=1.1, resolution=1, variable=currentwheelcontrol, orient="horizontal", length=60, width=10)
    wheelswitch.grid(row=1, column=25, columnspan=3)

    root.mainloop()



#draw the gui

main()