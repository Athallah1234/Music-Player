import os
import tkinter as tk
from tkinter import ttk, filedialog
from pygame import mixer
import random
import time
import eyed3
import threading

class AudioPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Player")

        self.playlist = []
        self.current_index = 0
        self.song_duration = 0
        self.play_pause_time = 0  # Initialize play_pause_time
        self.muted = False
        self.paused = False
        self.stopped = False

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        mixer.init()

        self.create_ui()

    def create_ui(self):
        # Playlist Treeview
        self.playlist_tree = ttk.Treeview(self.master, columns=("Name", "Artist", "Album", "Path", "Duration"), show="headings")
        self.playlist_tree.heading("Name", text="Name")
        self.playlist_tree.heading("Artist", text="Artist")  # Tambahkan kolom "Artist"
        self.playlist_tree.heading("Album", text="Album")
        self.playlist_tree.heading("Path", text="Path", anchor="center")
        self.playlist_tree.heading("Duration", text="Duration", anchor="center")
        self.playlist_tree.column("Name", width=200)
        self.playlist_tree.column("Artist", width=150)  # Sesuaikan lebar kolom "Artist"
        self.playlist_tree.column("Album", width=150)
        self.playlist_tree.column("Path", width=400)
        self.playlist_tree.column("Duration", width=100)
        self.playlist_tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Song", command=self.add_song).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Remove Song", command=self.remove_song).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Play", command=self.play).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="Stop", command=self.stop).grid(row=0, column=3, padx=10)
        ttk.Button(btn_frame, text="Pause/Resume", command=self.pause_resume).grid(row=0, column=4, padx=10)
        ttk.Button(btn_frame, text="Clear Playlist", command=self.clear_playlist).grid(row=0, column=5, padx=10)
        # Mute/Unmute Button
        ttk.Button(btn_frame, text="Mute/Unmute", command=self.toggle_mute).grid(row=0, column=8, padx=10)
        ttk.Button(btn_frame, text="Add Songs from Directory", command=self.add_songs_from_directory).grid(row=0, column=9, padx=10)

        # Volume Control
        ttk.Label(self.master, text="Volume").pack()
        self.volume_slider = ttk.Scale(self.master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack()

        # Song Information
        self.song_info_label = ttk.Label(self.master, text="Song Information")
        self.song_info_label.pack()

        # Song Duration Label
        ttk.Label(self.master, text="Duration").pack()
        self.duration_label = ttk.Label(self.master, text="0:00 / 0:00")
        self.duration_label.pack()

        # Timer for Current Playback Time
        self.timer_label = ttk.Label(self.master, text="0:00")
        self.timer_label.pack()

        # Next and Previous Buttons
        ttk.Button(self.master, text="Previous", command=self.play_previous).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.master, text="Next", command=self.play_next).pack(side=tk.RIGHT, padx=10)

        # Repeat and Shuffle
        self.repeat_var = tk.BooleanVar()
        ttk.Checkbutton(self.master, text="Repeat", variable=self.repeat_var).pack(side=tk.LEFT, padx=10)

    def get_song_album(self, file_path):
        audiofile = eyed3.load(file_path)
        if audiofile.tag and audiofile.tag.album:
            return audiofile.tag.album
        else:
            return "Unknown Album"

    def get_song_artist(self, file_path):
        audiofile = eyed3.load(file_path)
        if audiofile.tag and audiofile.tag.artist:
            return audiofile.tag.artist
        else:
            return "Unknown Artist"

    def on_closing(self):
        # Ask for confirmation before closing the application
        confirmed = tk.messagebox.askokcancel("Confirmation", "Are you sure you want to exit the application?")
        if confirmed:
            self.master.destroy()

    # Tambahkan metode berikut di dalam kelas AudioPlayer
    def clear_playlist(self):
        # Stop the currently playing music
        mixer.music.stop()

        # Reset Now Playing label
        self.song_info_label.config(text="Song Information")

        # Reset Duration label
        self.duration_label.config(text="0:00 / 0:00")

        self.timer_label.config(text="0:00")

        # Ask for confirmation before clearing the playlist
        confirmed = tk.messagebox.askyesno("Confirmation", "Are you sure you want to clear the playlist?")
        if confirmed:
            # Clear the playlist
            self.playlist = []
            self.playlist_tree.delete(*self.playlist_tree.get_children())

            # Reset the current index
            self.current_index = 0

    def add_songs_from_directory(self):
        # Create a new thread to run the file selection dialog
        thread = threading.Thread(target=self.select_directory_and_add_songs)
        thread.start()

    def add_song(self):
        # Create a new thread to run the file selection dialog
        thread = threading.Thread(target=self.select_file_and_add_song)
        thread.start()

    def select_directory_and_add_songs(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.add_songs_from_directory_in_thread(directory_path)

    def add_songs_from_directory_in_thread(self, directory_path):
        # Your existing logic for adding songs from a directory goes here
        audio_files = [file for file in os.listdir(directory_path) if self.is_valid_audio(file)]
        for audio_file in audio_files:
            file_path = os.path.join(directory_path, audio_file)
            duration = self.get_song_duration(file_path)
            if self.is_valid_duration(duration):
                file_name = os.path.basename(file_path)
                artist = self.get_song_artist(file_path)
                album = self.get_song_album(file_path)
                formatted_duration = self.format_time(duration)

                if file_path not in [song['path'] for song in self.playlist]:
                    self.playlist.append({"name": file_name, "artist": artist, "album": album, "path": file_path, "duration": formatted_duration})
                    self.playlist_tree.insert("", "end", values=(file_name, artist, album, file_path, formatted_duration))

        # Show a messagebox when the music loading is complete
        tk.messagebox.showinfo("Info", "Music loaded successfully!")

    def select_file_and_add_song(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_paths:
            # Take only the first selected file path
            file_path = file_paths[0]
            self.add_song_in_thread(file_path)

    def add_song_in_thread(self, file_path):
        # Your existing logic for adding a single song goes here
        duration = self.get_song_duration(file_path)
        if self.is_valid_duration(duration):
            file_name = os.path.basename(file_path)
            artist = self.get_song_artist(file_path)
            album = self.get_song_album(file_path)
            formatted_duration = self.format_time(duration)

            if file_path not in [song['path'] for song in self.playlist]:
                self.playlist.append({"name": file_name, "artist": artist, "album": album, "path": file_path, "duration": formatted_duration})
                self.playlist_tree.insert("", "end", values=(file_name, artist, album, file_path, formatted_duration))

    def is_valid_audio(self, file_path):
        return file_path.lower().endswith((".mp3", ".wav"))

    def is_valid_duration(self, duration):
        try:
            if isinstance(duration, str):
                minutes, seconds = map(int, duration.split(':'))
            elif isinstance(duration, (int, float)):
                minutes, seconds = divmod(int(duration), 60)
            else:
                return False

            return minutes >= 0 and seconds >= 0
        except ValueError:
            return False

    def remove_song(self):
        selected_item = self.playlist_tree.selection()
        if selected_item:
            # Stop the currently playing music
            mixer.music.stop()

            # Reset Now Playing label
            self.song_info_label.config(text="Song Information")

            # Reset Duration label
            self.duration_label.config(text="0:00 / 0:00")

            self.timer_label.config(text="0:00")

            index = self.playlist_tree.index(selected_item)
            self.playlist_tree.delete(selected_item)
            del self.playlist[index]

            # Update the current index if needed
            if index <= self.current_index:
                self.current_index -= 1

            # If the playlist is not empty, highlight the next song in the playlist
            if self.playlist:
                self.playlist_tree.selection_set(self.playlist_tree.get_children()[self.current_index])

            # If the playlist is empty, set the current index to 0
            else:
                self.current_index = 0

    def stop(self):
        if mixer.music.get_busy():
            mixer.music.stop()

        # Reset labels
        self.song_info_label.config(text="Song Information")
        self.duration_label.config(text="0:00 / 0:00")
        self.timer_label.config(text="0:00")
        self.stopped = True  # Set the stopped flag to True

    def pause_resume(self):
        if not self.paused:
            # Jika tidak sedang di-pause, pause dan catat waktu pause
            mixer.music.pause()
            self.paused = True
            self.play_pause_time = time.time()
        else:
            # Jika sedang di-pause, resume dan update waktu mulai
            mixer.music.unpause()
            self.paused = False
            self.play_pause_time = time.time()
            # Start Timer for Current Playback Time
            self.update_timer()

    def play(self):
        self.start_playing()

    def start_playing(self):
        if self.playlist:
            index = self.current_index
            selected_song = self.playlist[index]
            mixer.music.load(selected_song["path"])

            if not self.paused:
                mixer.music.play()

                # Update Song Information
                self.song_info_label.config(text=f"Now Playing: {selected_song['name']}")

                # Update window title
                self.master.title(f"Audio Player - {selected_song['name']}")

                # Set Song Duration
                self.song_duration = self.get_song_duration(selected_song["path"])

                # Update Duration Label
                self.duration_label.config(text=f"0:00 / {self.format_time(self.song_duration)}")

                # Update Play Start Time for Timer
                self.play_start_time = time.time()
                # Start Timer for Current Playback Time
                self.update_timer()
            else:
                # If paused, resume and update the timer
                mixer.music.unpause()
                self.paused = False
                self.play_start_time = time.time() - (self.play_start_time - self.play_pause_time)
                # Start Timer for Current Playback Time
                self.update_timer()
        else:
            tk.messagebox.showinfo("Info", "Playlist is empty. Add songs before playing.")

    def update_timer(self):
        if mixer.music.get_busy() and not self.paused and not self.stopped:
            current_time = time.time() - self.play_start_time

            if isinstance(self.song_duration, str):
                # If the input is in 'minutes:seconds' format, convert it to seconds
                minutes, seconds = map(int, self.song_duration.split(':'))
                self.song_duration = minutes * 60 + seconds

            if current_time >= self.song_duration:
                if self.repeat_var.get():
                    # Jika opsi pengulangan diaktifkan, ulangi lagu
                    self.play()
                else:
                    # Jika tidak ada pengulangan, stop pemutaran
                    self.stop()
                return

            self.timer_label.config(text=self.format_time(current_time))
            self.master.after(1000, self.update_timer)

            # Update Duration Label
            self.duration_label.config(text=f"{self.format_time(current_time)} / {self.format_time(self.song_duration)}")

        elif not self.stopped and not self.paused and self.repeat_var.get() and not mixer.music.get_busy():
            # Automatically play the same song when it finishes (if repeat is enabled)
            self.play()

        elif self.paused:
            # Song is paused, update the pause time
            self.play_pause_time = time.time()

        elif self.stopped:
            # Reset the stopped flag
            self.stopped = False

        else:
            # Song has ended, move to the next one
            self.play_next()

    def get_song_duration(self, file_path):
        return float(mixer.Sound(file_path).get_length())
    
    def format_time(self, seconds):
        if isinstance(seconds, str):
            # If the input is in 'minutes:seconds' or 'hours:minutes:seconds' format, convert it to seconds
            if ":" in seconds:
                parts = list(map(int, seconds.split(':')))
                if len(parts) == 2:
                    minutes, seconds = parts
                    seconds = minutes * 60 + seconds
                elif len(parts) == 3:
                    hours, minutes, seconds = parts
                    seconds = hours * 3600 + minutes * 60 + seconds

        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_volume(self, event=None):
        try:
            volume = int(self.volume_slider.get())
            if 0 <= volume <= 100:
                mixer.music.set_volume(volume / 100)
            else:
                tk.messagebox.showwarning("Warning", "Volume must be between 0 and 100.")
                # Optionally, reset the volume to a valid value
                self.volume_slider.set(50)
        except ValueError:
            tk.messagebox.showwarning("Warning", "Invalid volume value. Please enter a valid integer.")
            # Optionally, reset the volume to a valid value
            self.volume_slider.set(50)

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            # If muted, store the current volume and set the volume to 0
            self.muted_volume = int(self.volume_slider.get())
            self.volume_slider.set(0)
        else:
            # If unmuted, restore the previous volume
            self.volume_slider.set(self.muted_volume)

    def play_next(self):
        if self.playlist:
            if self.repeat_var.get():
                tk.messagebox.showwarning("Warning", "Repeat cannot be enabled at the same time.")
                return

            # Stop the currently playing music
            mixer.music.stop()

            # Increment the current index for the next song
            self.current_index = (self.current_index + 1) % len(self.playlist)

            # Highlight the next song in the playlist
            self.playlist_tree.selection_set(self.playlist_tree.get_children()[self.current_index])

            # Play the next song
            self.start_playing()
        else:
            # No songs in the playlist, show an info message or take other actions
            tk.messagebox.showinfo("Info", "Playlist is empty. Add songs before playing.")

    def play_previous(self):
        if self.playlist:
            # Stop the currently playing music
            mixer.music.stop()

            # Decrement the current index for the previous song
            self.current_index = (self.current_index - 1) % len(self.playlist)

            # Highlight the previous song in the playlist
            self.playlist_tree.selection_set(self.playlist_tree.get_children()[self.current_index])

            # Play the previous song
            self.start_playing()
        else:
            # No songs in the playlist, show an info message or take other actions
            tk.messagebox.showinfo("Info", "Playlist is empty. Add songs before playing.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.resizable(False, False)  # Hanya izinkan perubahan tinggi, bukan lebar
    root.mainloop()

