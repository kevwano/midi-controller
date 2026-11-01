# midi-controller
A program that allows the keyboard and mouse to be used as midi inputs. 

Installing loopMIDI is necessary to allow the computer to send MIDI inputs back to itself. Use the default port name.
https://www.tobias-erichsen.de/software/loopmidi.html
This port can then be accessed by any DAW or other software that needs a midi controller. 

Turn on the input using shift+r, and stop using esc. This program blocks keyboard input when on, so that keyboard shortcuts aren't triggered during recording.
Control note velocity or the modwheel using the mouse scroll wheel, and switch between them with the switch.

Change octaves using the arrow keys. 

Dependencies:
mido,
keyboard,
pynput
