import os
import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import requests
import youtube_dl
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.button import Button


class ButtonApp(App):

    def build(self):
        btn = Button(text="Push Me !")
        return btn

player = tk.Tk()
player.title("My Playlist")
player.geometry("710x400")
player.config(bg="lightblue")

def end_of_song():
    next_song()

pygame.mixer.music.set_endevent(pygame.USEREVENT)


var = tk.StringVar()
var.set("Select the song to play")

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)



volume = tk.Scale(player, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, label="Volume", bg="black", fg="white", font="Helvetica 13 bold")
volume.set(100)  # Set the default volume to 100 (maximum)
volume.pack(side=tk.LEFT, padx=10)



song_directory = filedialog.askdirectory()
os.chdir(song_directory)
songlist = os.listdir()

playing = tk.Listbox(player, font="Helvetica 12 bold", width=28, height="12", bg="black", fg="lightblue",
                     selectmode=tk.SINGLE)
for item in songlist:
    playing.insert(0, item)


def add_song_from_name():
    song_name = tk.simpledialog.askstring("Enter song name", "Enter the name of the song:")
    if song_name:
        try:

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(song_directory, song_name + '.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                search_query = song_name + ' lyrics'
                search_url = f'https://www.youtube.com/results?search_query={search_query}'
                res = requests.get(search_url)
                soup = BeautifulSoup(res.text, 'html.parser')
                vid_srcs = []
                for link in soup.find_all('a'):
                    if '/watch?v=' in link.get('href'):
                        vid_srcs.append('https://www.youtube.com' + link.get('href'))
                video_url = vid_srcs[0]
                ydl.download([video_url])
                playing.insert(0, song_name + '.mp3')
        except:
            messagebox.showerror("Error", "Could not download the song.")

add_song_btn = tk.Button(player, width=8, height=4, font="Helvetica 13 bold", text="Add Song",
                         command=add_song_from_name, bg="#2c3e50", fg="#ecf0f1")
add_song_btn.pack(side=tk.RIGHT, padx=10)


def next_song():
    current_index = playing.curselection()[0]
    next_index = (current_index + 1) % playing.size()
    playing.selection_clear(0, "end")
    playing.activate(next_index)
    playing.selection_set(next_index, last=None)
    play()


def back_song():
    current_index = playing.curselection()[0]
    back_index = (current_index - 1) % playing.size()
    playing.selection_clear(0, "end")
    playing.activate(back_index)
    playing.selection_set(back_index, last=None)
    play()

def update_timeline(value):
    pygame.mixer.music.set_pos(int(value))

timeline = tk.Scale(player, width=9, from_=0, to=100, orient=tk.HORIZONTAL, command=update_timeline, bg="black", fg="black")
timeline.pack(side=tk.BOTTOM, fill=tk.X, padx=10)

def update_timeline_progress():
    timeline.set(pygame.mixer.music.get_pos()/pygame.mixer.music.get_length() * end_of_song())
    player.after(100, update_timeline_progress)

player.after(100, update_timeline_progress)





def play():
    pygame.mixer.music.load(os.path.join(song_directory, playing.get(tkinter.ACTIVE)))
    name = playing.get(tkinter.ACTIVE)
    var.set(f"{name[:16]}..." if len(name) > 18 else name)
    pygame.mixer.music.play()


def pause():
    pygame.mixer.music.pause()


def resume():
    pygame.mixer.music.unpause()


text = tk.Label(player, font="Helvetica 20 bold", textvariable=var, bg="gray")
text.pack(pady=10)
playing.pack(pady=10)

back_song_btn = tk.Button(player, width=3, height=1, font="Helvetica 20 bold", text="<", command=back_song,
                          bg="#2c3e50", fg="#ecf0f1")
back_song_btn.pack(side=tk.LEFT, padx=10)

pause_btn = tk.Button(player, width=4, height=1, font="Didot 20 bold", text="II", command=pause, bg="red",
                      fg="black")
pause_btn.pack(side=tk.LEFT, padx=10)
play_btn = tk.Button(player, width=5, height=1, font="Futura 20 bold", text="♪", command=play, bg="green",
                     fg="black")
play_btn.pack(side=tk.LEFT, padx=10)

resume_btn = tk.Button(player, width=4, height=1, font="Helvetica 20 bold", text="►", command=resume, bg="gold",
                       fg="black")
resume_btn.pack(side=tk.LEFT, padx=10)

next_song_btn = tk.Button(player, width=3, height=1, font="Helvetica 20 bold", text=">", command=next_song,
                          bg="#2c3e50", fg="#ecf0f1")
next_song_btn.pack(side=tk.LEFT, padx=10)



player.mainloop()