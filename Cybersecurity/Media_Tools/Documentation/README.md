# 🎵 Media Applications Suite 🎬

A collection of two powerful media applications for playing and downloading multimedia content.

## 📁 Applications Included

### 🎵 **Media Player** (`media_player.py`)
- Play **MP3, WAV, OGG, M4A** audio files
- Play **MP4, AVI, MOV, MKV, WMV** video files  
- Modern GUI with play/pause/stop controls
- Volume slider and progress tracking
- Real-time video display

### 📥 **YouTube Playlist Downloader** (`youtube_downloader.py`)
- Download entire YouTube playlists as **MP3** or **MP4**
- **Network diagnostics** to troubleshoot connection issues
- **SSL troubleshooting** for handshake failures
- Multiple quality options and progress tracking
- Enhanced error handling and logging

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Applications
```bash
# Media Player
python media_player.py

# YouTube Downloader  
python youtube_downloader.py
```

## 🔧 YouTube Downloader Features

### **Network Diagnostics**
- **🌐 Ping YouTube** - Test basic connectivity
- **🔍 Check DNS** - Verify domain resolution  
- **🔐 Test SSL** - Try different SSL configurations
- **📺 Test yt-dlp** - Find working download settings

### **Smart Download Options**
- **Auto-detection** of optimal connection settings
- **SSL troubleshooting** for handshake failures
- **Multiple retry methods** for network issues
- **Detailed logging** of all operations

### **Format Options**
- **MP3**: High-quality audio (192 kbps)
- **MP4**: Video in multiple quality options (best, 720p, 480p, 360p)

## 💡 Troubleshooting

### If YouTube downloads fail:
1. **Run network diagnostics first** (in the YouTube downloader)
2. **Check each diagnostic test**:
   - Ping should show connectivity ✅
   - DNS should resolve YouTube domains ✅  
   - SSL should find working cipher ✅
   - yt-dlp should retrieve test video ✅
3. **If diagnostics pass**, downloads should work
4. **If diagnostics fail**, check firewall/proxy settings

### Common Issues & Solutions:
- **SSL Handshake Failure**: Use the built-in SSL diagnostics
- **Connection Timeout**: Check firewall and network settings
- **DNS Issues**: Try different DNS servers (8.8.8.8, 1.1.1.1)
- **Proxy/Corporate Network**: May need VPN or alternative network

## 📋 File Structure
```
📁 spammer/
├── 🎵 media_player.py          # Audio/Video player
├── 📥 youtube_downloader.py    # Playlist downloader with diagnostics
├── 📄 requirements.txt         # All dependencies
├── 📖 README.md               # This documentation
├── 📘 MEDIA_README.md         # Media player specific docs
└── 📙 YOUTUBE_README.md       # YouTube downloader specific docs
```

## 🎯 Key Features Summary

### **Media Player:**
✅ Multi-format audio/video support  
✅ Clean, modern GUI interface  
✅ Real-time progress tracking  
✅ Volume control and seeking  

### **YouTube Downloader:**
✅ Full playlist downloading  
✅ Network troubleshooting tools  
✅ SSL/connection diagnostics  
✅ Multiple format/quality options  
✅ Comprehensive error logging  

## 🔒 Legal Notice
- **Personal use only** - respect copyright laws
- **Educational content** downloading is generally acceptable  
- **Check local laws** regarding content downloading
- **Commercial use** may require permissions

Both applications are ready to use and include comprehensive error handling and user-friendly interfaces!