from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import os
import time
import tkinter.ttk as ttk


# CREATE GUI WINDOW
root = Tk()
root.title("MP3 Player")
root.geometry("600x400")


# INITIALIZE PYGAME FOR AUDIO
pygame.mixer.init()


# GLOBAL VARIABLES
is_paused = False
is_stopped = True
playlist = []
current_song_title = None
current_song_dir = None
current_song_index = None


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
    global is_paused, is_stopped, current_song_title, current_song_dir, current_song_index
    
    stop_song()

    current_selection = playlist_box.curselection()

    if current_selection:
        is_paused = False
        is_stopped = False
        current_song_index = current_selection[0]
        current_song_title = playlist[current_song_index]['title']
        current_song_dir = playlist[current_song_index]['file_dir']
        song_slider.config(value=0)
        status_bar.config(text='')
        pygame.mixer.music.load(current_song_dir)
        pygame.mixer.music.play(loops=0)
        
        play_time()


def stop_song():
    global is_stopped

    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')
    song_slider.config(value=0)
    is_stopped = True


def pause_song():
    global is_paused

    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        pygame.mixer.music.pause()
        is_paused = True
    

def next_song():
    global current_song_index, current_song_title, current_song_dir, is_stopped, is_paused

    stop_song()

    if current_song_index < len(playlist)-1:
        current_song_index+=1
    else:
        current_song_index = 0
    
    current_song_title = playlist[current_song_index]['title']
    current_song_dir = playlist[current_song_index]['file_dir']

    playlist_box.selection_clear(0, END)
    playlist_box.activate(current_song_index)
    playlist_box.selection_set(current_song_index, last=None)

    song_slider.config(value=0)
    status_bar.config(text='')

    is_paused = False
    is_stopped = False

    pygame.mixer.music.load(current_song_dir)
    pygame.mixer.music.play(loops=0)


def previous_song():
    global current_song_index, current_song_title, current_song_dir, is_stopped, is_paused

    stop_song()

    if current_song_index > 0:
        current_song_index-=1
    else:
        current_song_index = len(playlist)-1

    current_song_title = playlist[current_song_index]['title']
    current_song_dir = playlist[current_song_index]['file_dir']

    playlist_box.selection_clear(0, END)
    playlist_box.activate(current_song_index)
    playlist_box.selection_set(current_song_index, last=None)

    song_slider.config(value=0)
    status_bar.config(text='')
    
    is_paused = False
    is_stopped = False

    pygame.mixer.music.load(current_song_dir)
    pygame.mixer.music.play(loops=0)


def play_time():
    global is_stopped, is_paused, current_song_dir

    if is_stopped:
        return

    song_mut = MP3(current_song_dir)
    raw_song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(raw_song_length))
    counter = int(song_slider.get())
    current_time = time.strftime('%M:%S', time.gmtime(counter))

    if not is_paused:
        counter += 1
        song_slider.config(to=raw_song_length, value=counter)
        current_time = time.strftime('%M:%S', time.gmtime(counter))

    if counter > 0:
        status_bar.config(text=f'Time Elapsed: {current_time} of {converted_song_length}  ')
        song_slider.config(value=counter)

        if current_time == converted_song_length:
            next_song()
    
    status_bar.after(1000, play_time)


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


def slide(x):
    global is_stopped, current_song_dir

    if not is_stopped:
        pygame.mixer.music.load(current_song_dir)
        pygame.mixer.music.play(loops=0, start=song_slider.get())


def up():
    global current_song_index

    current_selection = playlist_box.curselection()[0]
    if current_selection == 0:
        pass
    else:
        to_move = playlist[current_selection]
        playlist.pop(current_selection)
        playlist.insert(current_selection-1, to_move)
        
        playlist_box.delete(0, END)
        for song in playlist:
            playlist_box.insert(END, song['title'])

        playlist_box.activate(current_selection-1)
        playlist_box.selection_set(current_selection-1, last=None)
        current_song_index = current_selection-1
        # print(playlist)


def down():
    global current_song_index

    current_selection = playlist_box.curselection()[0]
    if current_selection == len(playlist)-1:
        pass
    else:
        to_move = playlist[current_selection]
        playlist.pop(current_selection)
        playlist.insert(current_selection+1, to_move)
        
        playlist_box.delete(0, END)
        for song in playlist:
            playlist_box.insert(END, song['title'])

        playlist_box.activate(current_selection+1)
        playlist_box.selection_set(current_selection+1, last=None)
        current_song_index = current_selection+1
        # print(playlist)


# GUI WINDOW MENU
main_menu = Menu(root)
root.config(menu=main_menu)

# Create Playlist menu
playlist_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Playlist", menu=playlist_menu)
playlist_menu.add_command(label="Add One Song", command=add_song)
playlist_menu.add_command(label="Add Multiple Songs", command=add_multiple)
playlist_menu.add_separator()
playlist_menu.add_command(label="Delete Song", command=delete_song)
playlist_menu.add_command(label="Clear Playlist", command=delete_all_songs)


# GUI WIDGETS AND FEATURES

# Frame to hold Playlist, Volume Control, Audio Controls 
main_frame = Frame(root)
main_frame.pack(pady=20)

# Playlist box to display current playlist song titles
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

# Volume frame to hold Volume Slider
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

# Volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, value=1, orient=VERTICAL, length=125, command=volume) #add 'value' attribute and to set a default starting value (between from_ and to values)
volume_slider.pack(pady=10)

# Move song
order_frame = LabelFrame(main_frame, text="Order")
order_frame.grid(row=0, column=2)

move_up_button = Button(order_frame, text="Up", command=up)
move_up_button.pack(padx=5, pady=5)
move_down_button = Button(order_frame, text="Down", command=down)
move_down_button.pack(padx=5, pady=5)

# Song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, value=0, orient=HORIZONTAL, length=360, command=slide)
song_slider.grid(row=1, column=0, pady=10)

# Control frame to hold Audio Control buttons
control_frame = Frame(main_frame)
control_frame.grid(row=2, column=0, pady=20)

# Audio Control buttons
back_btn_img = PhotoImage(file="images/back50.png")
back_btn = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
back_btn.grid(row=0, column=0, padx=10)

forward_btn_img = PhotoImage(file="images/forward50.png")
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
forward_btn.grid(row=0, column=1, padx=10)

play_btn_img = PhotoImage(file="images/play50.png")
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_song)
play_btn.grid(row=0, column=2, padx=10)

pause_btn_img = PhotoImage(file="images/pause50.png")
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_song)
pause_btn.grid(row=0, column=3, padx=10)

stop_btn_img = PhotoImage(file="images/stop50.png")
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop_song)
stop_btn.grid(row=0, column=4, padx=10)

# Status bar
status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)





root.mainloop()