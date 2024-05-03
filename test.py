import os
from pynput.keyboard import Key, Listener, KeyCode
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# requirements pynput pycaw
# open with pythonw3.12 in 
# Win + R -> shell:startup -> open with pythonw3.12

"""
Layer 1
fn 13 -> open spotify
fn 14 -> open discord
fn 15 -> open vscode
fn 16 -> open chrome

fn 23 -> spotify volume up
fn 24 -> spotify volume down

fn 22 reserved as modifier
"""
import tkinter as tk

def getClipboardText():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    ctx = root.clipboard_get()
    root.quit()
    return ctx
# TODO: Text formatting (all upper/lower)

class MacroPad():
    def __init__(self, debugMode = False) -> None:
        self.previousEvent = None
        self.debugMode = debugMode
        self.attempt_spotify_setup()
    
    def attempt_spotify_setup(self):
        if self.debugMode: print("Attempting to link to Spotify Volume Controller")
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == "Spotify.exe":
                self.spotifyVolume = (float(volume.GetMasterVolume()) * 100)
                self.spotifyKnob = volume
    
    def sp_volume_up(self):
        try:
            newVolume = self.spotifyVolume + 5
            if newVolume > 100: newVolume = 100
            self.spotifyKnob.SetMasterVolume(newVolume/100, None)
            self.spotifyVolume = newVolume
            if self.debugMode: print(f"Raising Spotify Volume to {newVolume}")
        except:
            if self.debugMode: print(f"[ERROR] Raising Spotify Volume Failed")
            self.attempt_spotify_setup()
    
    def sp_volume_down(self):
        try:
            newVolume = self.spotifyVolume - 5
            if newVolume < 0: newVolume = 0
            self.spotifyKnob.SetMasterVolume(newVolume/100, None)
            self.spotifyVolume = newVolume
            if self.debugMode: print(f"Lowering Spotify Volume to {newVolume}")
        except:
            if self.debugMode: print(f"[ERROR] Lowering Spotify Volume Failed")
            self.attempt_spotify_setup()
    
    def on_press(self, key):
        if key == Key.f13:
            if self.debugMode: print(f"Opening Spotify")
            os.startfile(r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.235.663.0_x64__zpdnekdrzrea0\Spotify.exe")
        if key == Key.f14:
            if self.debugMode: print(f"Opening Discord")
            os.startfile(r"C:\Users\joshh\OneDrive\Desktop\Discord.lnk")
        if key == Key.f15:
            if self.debugMode: print(f"Opening VSCode")
            os.startfile(r"C:\Users\joshh\OneDrive\Desktop\Visual Studio Code.lnk")
        if key == Key.f16:
            if self.debugMode: print(f"Opening Chrome")
            os.startfile(r"C:\Users\joshh\OneDrive\Desktop\Chrome.lnk")
        if key == Key.f17:
            pass
        if key == Key.f18:
            pass
        if key == Key.f19:
            pass
        if key == Key.f20:
            pass
        if key == Key.f21:
            pass
        if key == Key.f23:
            pass
        if key == Key.f24:
            if self.debugMode: print(f"Attempting to lower Spotify volume")
            self.sp_volume_down()
        if key== Key.f23:
            if self.debugMode: print(f"Attempting to raise Spotify volume")
            self.sp_volume_up()
            
        
        
        if self.previousEvent: # Combo Keys
            
            # D1
            if self.previousEvent == Key.f13 and key == Key.f14:
                pass
        
        self.previousEvent = key

    def on_release(self, key):
        if key == Key.esc:
            return False

mp = MacroPad(True)
with Listener(on_press=mp.on_press, on_release=mp.on_release) as listener:
    listener.join()