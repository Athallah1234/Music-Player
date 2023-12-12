# Audio Player Application

This is a simple audio player application built using Python and the Tkinter library. The application allows you to create and manage playlists, play audio files, control playback (play, pause, stop, next, previous), adjust volume, and more.

## Features

- **Playlist Management:** Add individual songs or entire directories to the playlist.
- **Play Controls:** Play, pause, stop, skip to the next or previous track.
- **Volume Control:** Adjust the volume with a slider.
- **Song Information:** Display information about the currently playing song.
- **Duration Display:** Shows the current playback time and total duration of the song.
- **Mute/Unmute:** Toggle mute functionality.
- **Repeat:** Enable or disable repeat functionality.
- **Clear Playlist:** Clear the entire playlist.

## How to Use

1. **Adding Songs:**
   - Click the "Add Song" button to add individual songs.
   - Use "Add Songs from Directory" to add all compatible audio files from a directory.
2. **Playlist Management:**
   - Use "Remove Song" to remove a selected song from the playlist.
   - Click "Clear Playlist" to remove all songs from the playlist.
3. **Playback Controls:**
   - Use "Play" to start playback.
   - "Pause/Resume" to pause or resume playback.
   - "Stop" to stop playback.
4. **Volume Control:**
   - Adjust the volume using the volume slider.
5. **Navigation:**
   - Use "Next" and "Previous" buttons to navigate through the playlist.
6. **Repeat:**
   - Check the "Repeat" checkbox to enable repeat functionality.
7. **Mute/Unmute:**
   - Click "Mute/Unmute" to toggle mute functionality.
8. **Exiting the Application:**
   - Click the close button to exit the application. A confirmation dialog will appear.
  
## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- pygame library
- eyed3 library

## Installation

1. Clone or download the repository.
2. Install the required libraries:
   `` bash
   pip install pygame eyed3
   ``
3. Run the application:
   `` bash
   python audio_player.py
   ``

## Contributing

If you'd like to contribute to the development of this audio player, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Description of your changes'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request on the main repository.

## License

This audio player is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Code Style

To maintain a consistent code style throughout the project, we follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide. Please ensure that your contributions adhere to this style guide.

## Release Process

When preparing for a new release, follow these steps:

1. Update the version number in the code.
2. Update the [Changelog](CHANGELOG.md) with details of changes.
3. Create a new GitHub release.
4. Update the installation instructions in the README if necessary.

## Acknowledgments

- Special thanks to the developers of Tkinter, pygame, and eyed3 for providing the tools to create this application.
- This project was inspired by a desire for a simple and customizable audio player.

Feel free to customize, improve, and share this audio player. Happy coding!
