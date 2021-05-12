from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import os
import time

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")


# GLOBAL VARIABLES
is_paused = False
playlist = []

# FUNCTIONS
def add_song():
    song_dir = filedialog.askopenfilename(initialdir='audio/', filetypes=[('MP3 Files', '*.mp3')])
    song_title = os.path.basename(song_dir).split('.')[0]
    playlist_box.insert(END, song_title)
    playlist.append(dict(title=song_title, file_dir=song_dir))


def add_multiple():
    songs = filedialog.askopenfilenames(initialdir='audio/', filetypes=[('MP3 Files', '*.mp3')])

    for song in songs:
        song_title = os.path.basename(song).split('.')[0]
        playlist_box.insert(END, song_title)
        playlist.append(dict(title=song_title, file_dir=song))


def delete_song():
    index = playlist_box.curselection()
    playlist.pop(index[0])
    playlist_box.delete(ANCHOR)


def delete_all_songs():
    playlist.clear()
    playlist_box.delete(0, END)


def play_song():
    global is_paused
    is_paused = False
    current_selection = playlist_box.curselection()
    selected_song = playlist[current_selection[0]]['file_dir']
    pygame.mixer.music.load(selected_song)
    pygame.mixer.music.play(loops=0)
    
    play_time()


def stop_song():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')


def pause_song():
    global is_paused

    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        pygame.mixer.music.pause()
        is_paused = True
    

def next_song():
    current_song = playlist_box.curselection()

    if current_song[0] < len(playlist)-1:
        next_index = current_song[0]+1
    else:
        next_index = 0
    
    next_song_dir = playlist[next_index]['file_dir']

    playlist_box.selection_clear(0, END)
    playlist_box.activate(next_index)
    playlist_box.selection_set(next_index, last=None)
    
    pygame.mixer.music.load(next_song_dir)
    pygame.mixer.music.play(loops=0)


def previous_song():
    current_song = playlist_box.curselection()

    if current_song[0] > 0:
        prev_index = current_song[0]-1
    else:
        prev_index = len(playlist)-1

    prev_song_dir = playlist[prev_index]['file_dir']

    playlist_box.selection_clear(0, END)
    playlist_box.activate(prev_index)
    playlist_box.selection_set(prev_index, last=None)
    
    pygame.mixer.music.load(prev_song_dir)
    pygame.mixer.music.play(loops=0)


def play_time():
    current_position = pygame.mixer.music.get_pos()/1000
    current_time = time.strftime('%M:%S', time.gmtime(current_position))

    current_selection = playlist_box.curselection()
    selected_song = playlist[current_selection[0]]['file_dir']

    song_mut = MP3(selected_song)
    raw_song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(raw_song_length))

    test_label.config(text=converted_song_length)

    if current_position >= 1:
        status_bar.config(text=f'Time Elapsed: {current_time} of {converted_song_length}  ')
    
    status_bar.after(1000, play_time)



# Initialize PyGame

pygame.mixer.init()

# Create playlist box
playlist_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.pack(pady=20)



# Create media control buttons
# Control frame to group the buttons in
control_frame = Frame(root)
control_frame.pack(pady=20)

# Define button images
back_btn_img = PhotoImage(file="images/back50.png")
forward_btn_img = PhotoImage(file="images/forward50.png")
play_btn_img = PhotoImage(file="images/play50.png")
pause_btn_img = PhotoImage(file="images/pause50.png")
stop_btn_img = PhotoImage(file="images/stop50.png")

# Create the actual buttons and link them to the control frame
back_btn = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_song)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_song)
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop_song)

# Place the buttons on the screen
back_btn.grid(row=0, column=0, padx=10)
forward_btn.grid(row=0, column=1, padx=10)
play_btn.grid(row=0, column=2, padx=10)
pause_btn.grid(row=0, column=3, padx=10)
stop_btn.grid(row=0, column=4, padx=10)


# Create menu

main_menu = Menu(root)
root.config(menu=main_menu)

# Create Add Song sub-menu
playlist_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Playlist", menu=playlist_menu)

playlist_menu.add_command(label="Add One Song", command=add_song)
playlist_menu.add_command(label="Add Multiple Songs", command=add_multiple)
playlist_menu.add_separator()
playlist_menu.add_command(label="Delete Song", command=delete_song)
playlist_menu.add_command(label="Clear Playlist", command=delete_all_songs)

# Create status bar

status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)






# Temp label to for output testing
test_label = Label(root, text="")
test_label.pack(pady=20)


root.mainloop()