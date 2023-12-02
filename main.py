import sounddevice as sd
import soundfile as sf
import edge_tts
import asyncio
from threading import Thread
import customtkinter
from tkinter import DISABLED,ACTIVE,END

last_text = ""
loop = asyncio.get_event_loop()

def play_in_mic():
        button.configure(state=DISABLED)
        data, fs = sf.read("tts.mp3", dtype='float32')
        sd.play(data,fs,device=15)
        sd.wait()
        button.configure(state=ACTIVE)

def play_in_speaker():
        data, fs = sf.read("tts.mp3", dtype='float32')
        sd.play(data,fs)
        sd.wait()
        

async def tts(text,voice) -> None:
        global last_text
        if (last_text != text):
            communicate = edge_tts.Communicate(text,volume="+500%",voice=voice)
            button.configure(state=DISABLED)
            await communicate.save("tts.mp3")
            last_text = text
        Thread(target=play_in_mic).start()
        Thread(target=play_in_speaker).start()
        

def run_tts():
        
        loop.run_until_complete(tts(tts_text.get(),option.get()))

def run_button():
       Thread(target=run_tts).start()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x300")
app.resizable(False, False)

def reset():
    tts_text.delete(0, END)
    tts_text.insert(0, "")
    pass

option = customtkinter.CTkOptionMenu(master=app, width=250, height=30, values=["fa-IR-DilaraNeural", "fa-IR-FaridNeural"])
option.place(relx=0.5, rely=0.17, anchor=customtkinter.CENTER)

tts_text = customtkinter.CTkEntry(master=app, width=250, height=150)
tts_text.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=app, width=195, height=30,text="Run Tts",command=run_button)
button.place(relx=0.43, rely=0.83, anchor=customtkinter.CENTER)

reset_button = customtkinter.CTkButton(master=app, width=50, height=30,text="Reset",command=reset)
reset_button.place(relx=0.75, rely=0.83, anchor=customtkinter.CENTER)

app.mainloop()
