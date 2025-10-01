# MP3 & MP4 Media Player

A full-featured GUI media player that supports both audio and video files.

## Features

### Audio Support
- **MP3, WAV, OGG, M4A** formats
- Play, pause, stop controls
- Volume control
- Duration display
- Progress tracking

### Video Support  
- **MP4, AVI, MOV, MKV, WMV** formats
- Video playback with controls
- Resize to fit display window
- Frame-by-frame rendering

### User Interface
- Modern dark theme GUI
- File browser integration
- Real-time progress bar
- Time display (current/total)
- Volume slider
- Video display area

## Installation

1. **Install required packages:**
```bash
pip install -r media_requirements.txt
```

2. **Run the media player:**
```bash
python media_player.py
```

## How to Use

1. **Open File**: Click "Open File" to browse and select your media
2. **Play/Pause**: Toggle playback with the Play/Pause button  
3. **Stop**: Stop playback and return to beginning
4. **Volume**: Adjust volume with the slider (0-100%)
5. **Progress**: View current playback position

## Supported Formats

**Audio:**
- MP3 (MPEG Audio Layer 3)
- WAV (Waveform Audio File)
- OGG (Ogg Vorbis)
- M4A (MPEG-4 Audio)

**Video:**
- MP4 (MPEG-4 Video)
- AVI (Audio Video Interleave)
- MOV (QuickTime Movie)
- MKV (Matroska Video)
- WMV (Windows Media Video)

## Technical Details

- **GUI Framework**: tkinter (built-in Python)
- **Audio Engine**: pygame mixer
- **Video Engine**: OpenCV (cv2)
- **Image Processing**: PIL/Pillow
- **Metadata**: mutagen library
- **Threading**: For smooth video playback

## Controls

- **Open File**: Browse and load media files
- **Play/Pause**: Start or pause playback
- **Stop**: Stop and reset to beginning
- **Volume Slider**: Adjust audio volume
- **Progress Bar**: Shows current playback position

## Notes

- Video files display in a 640x360 window
- Audio files show a music note display
- Progress tracking works for both audio and video
- Volume control affects audio playback
- Supports most common media formats

The player provides a clean, user-friendly interface for enjoying your media files!