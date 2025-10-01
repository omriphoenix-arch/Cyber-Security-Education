# 🎵 YouTube Playlist Downloader 🎬

A powerful GUI application to download entire YouTube playlists as MP3 (audio) or MP4 (video) files.

## ✨ Features

### 📱 User Interface
- **Modern GUI** with dark theme
- **Real-time progress** tracking
- **Playlist analysis** before download
- **Batch downloading** of entire playlists

### 🎵 Audio Downloads (MP3)
- **High-quality MP3** extraction (192 kbps)
- **Audio-only** downloads (smaller file sizes)
- **Automatic conversion** from video to audio
- **ID3 tags** preserved when available

### 🎬 Video Downloads (MP4)
- **Multiple quality options**: Best, 720p, 480p, 360p, 240p, Worst
- **MP4 format** for maximum compatibility
- **Original video quality** preservation
- **Fast downloading** with resume support

### 📋 Playlist Support
- **Entire playlist** downloading
- **Playlist information** preview
- **Video count** and title display
- **Channel information** extraction

## 🚀 Installation

### 1. Install Required Packages
```bash
pip install -r youtube_requirements.txt
```

### 2. Install FFmpeg (Required for MP3 conversion)

**Windows:**
- Download FFmpeg from https://ffmpeg.org/download.html
- Extract and add to your PATH, or place in the same directory as the script

**Alternative (using conda):**
```bash
conda install ffmpeg
```

### 3. Run the Application
```bash
python youtube_downloader.py
```

## 📖 How to Use

### Step 1: Enter Playlist URL
1. **Copy a YouTube playlist URL** (e.g., https://youtube.com/playlist?list=...)
2. **Paste it** in the "Playlist URL" field
3. **Click "Analyze Playlist"** to get information

### Step 2: Configure Settings
- **Format**: Choose MP3 (audio) or MP4 (video)
- **Quality**: Select download quality (Best recommended)
- **Location**: Choose where to save files

### Step 3: Download
1. **Click "Start Download"** to begin
2. **Monitor progress** in real-time
3. **Files save** to your chosen directory

## 📝 Supported URLs

### ✅ Valid YouTube URLs:
- `https://youtube.com/playlist?list=PLxxxxxx`
- `https://www.youtube.com/watch?v=xxxxx&list=PLxxxxxx`
- `https://youtu.be/xxxxx?list=PLxxxxxx`
- `https://m.youtube.com/playlist?list=PLxxxxxx`

### ❌ Not Supported:
- Single video URLs (without playlist)
- Private/unlisted playlists
- Age-restricted content
- Region-blocked videos

## ⚙️ Features Explained

### 🔍 Playlist Analysis
- **Analyzes up to 50 videos** for preview
- **Shows playlist title** and channel
- **Displays video count** and first 10 titles
- **Validates URL** before downloading

### 📊 Progress Tracking
- **Real-time download progress** with percentages
- **Download speed** display
- **Current file** being processed
- **Success/error notifications**

### 📁 File Organization
- **Automatic naming** using video titles
- **Clean filenames** (removes invalid characters)
- **Organized structure** in chosen directory
- **No duplicate downloads** (skips existing files)

## 🛠️ Technical Details

### Dependencies
- **yt-dlp**: Modern YouTube downloader (fork of youtube-dl)
- **ffmpeg**: Audio/video conversion
- **tkinter**: GUI framework (built-in Python)
- **threading**: Background downloads

### File Formats
- **MP3**: 192 kbps quality, ID3v2 tags
- **MP4**: Original quality or selected resolution
- **Automatic extension**: Based on selected format

### Performance
- **Multi-threaded**: Downloads don't freeze the GUI
- **Memory efficient**: Streams large files
- **Resume support**: Can continue interrupted downloads
- **Error handling**: Continues with next video on errors

## 🚨 Important Notes

### Legal Usage
- **Personal use only** - respect copyright laws
- **Educational content** downloading is generally acceptable
- **Commercial use** may require permission
- **Check local laws** regarding content downloading

### Requirements
- **Internet connection** for downloading
- **Sufficient storage space** for files
- **FFmpeg installed** for MP3 conversion
- **Python 3.7+** recommended

### Troubleshs