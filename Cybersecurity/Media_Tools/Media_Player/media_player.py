"""
MP3 and MP4 Media Player
A GUI-based media player that can play audio (MP3, WAV, etc.) and video (MP4, AVI, etc.) files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import math

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 & MP4 Media Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Media variables
        self.current_file = None
        self.file_type = None  # 'audio' or 'video'
        self.is_playing = False
        self.is_paused = False
        self.video_cap = None
        self.video_thread = None
        self.duration = 0
        self.current_position = 0
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Media Player", 
                              font=("Arial", 24, "bold"), 
                              fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Video display area
        self.video_frame = tk.Frame(main_frame, bg="#34495e", width=640, height=360)
        self.video_frame.pack(pady=(0, 20))
        self.video_frame.pack_propagate(False)
        
        self.video_label = tk.Label(self.video_frame, bg="#34495e", 
                                   text="No media loaded\nClick 'Open File' to start",
                                   font=("Arial", 16), fg="#bdc3c7")
        self.video_label.pack(expand=True)
        
        # File info frame
        info_frame = tk.Frame(main_frame, bg="#2c3e50")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_info_label = tk.Label(info_frame, text="No file selected", 
                                       font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.file_info_label.pack()
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.time_label = tk.Label(progress_frame, text="00:00 / 00:00", 
                                  font=("Arial", 10), fg="#bdc3c7", bg="#2c3e50")
        self.time_label.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(progress_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, variable=self.progress_var,
                                     command=self.on_progress_change)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg="#2c3e50")
        controls_frame.pack(pady=(0, 20))
        
        # Control buttons
        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", 
                       "relief": "flat", "padx": 20, "pady": 5}
        
        self.open_btn = tk.Button(controls_frame, text="Open File", 
                                 command=self.open_file, **button_style)
        self.open_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_pause_btn = tk.Button(controls_frame, text="Play", 
                                       command=self.toggle_play_pause, 
                                       state=tk.DISABLED, **button_style)
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(controls_frame, text="Stop", 
                                 command=self.stop, state=tk.DISABLED, **button_style)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(main_frame, bg="#2c3e50")
        volume_frame.pack(pady=(0, 10))
        
        tk.Label(volume_frame, text="Volume:", font=("Arial", 10), 
                fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=70)
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, variable=self.volume_var,
                                     command=self.on_volume_change)
        self.volume_scale.pack(side=tk.LEFT, padx=(10, 0))
        
        # Set initial volume
        pygame.mixer.music.set_volume(0.7)
        
    def open_file(self):
        """Open file dialog to select media file"""
        file_types = [
            ("All Supported", "*.mp3 *.wav *.mp4 *.avi *.mov *.mkv"),
            ("Audio Files", "*.mp3 *.wav *.ogg *.m4a"),
            ("Video Files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=file_types
        )
        
        if filename:
            self.load_file(filename)
    
    def load_file(self, filename):
        """Load and prepare media file"""
        self.current_file = filename
        
        # Determine file type
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.mp3', '.wav', '.ogg', '.m4a']:
            self.file_type = 'audio'
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
            self.file_type = 'video'
        else:
            messagebox.showerror("Error", "Unsupported file format")
            return
        
        # Get file info and duration
        self.get_media_info(filename)
        
        # Update UI
        self.file_info_label.config(text=f"Loaded: {os.path.basename(filename)}")
        self.play_pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Clear video display for audio files
        if self.file_type == 'audio':
            self.video_label.config(text=f"♪ Audio File ♪\n{os.path.basename(filename)}")
        
    def get_media_info(self, filename):
        """Get media duration and other info"""
        try:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.mp3':
                audio = MP3(filename)
                self.duration = audio.info.length
            elif ext == '.mp4':
                audio = MP4(filename)
                self.duration = audio.info.length
            else:
                # For other formats, use cv2 to get duration
                if self.file_type == 'video':
                    cap = cv2.VideoCapture(filename)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    self.duration = frame_count / fps if fps > 0 else 0
                    cap.release()
                else:
                    self.duration = 0
        except:
            self.duration = 0
    
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if not self.current_file:
            return
            
        if self.is_playing:
            self.pause()
        else:
            self.play()
    
    def play(self):
        """Start playing media"""
        if not self.current_file:
            return
            
        try:
            if self.file_type == 'audio':
                if self.is_paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.load(self.current_file)
                    pygame.mixer.music.play()
                
            elif self.file_type == 'video':
                if not self.is_paused:
                    self.video_cap = cv2.VideoCapture(self.current_file)
                
                if self.video_thread is None or not self.video_thread.is_alive():
                    self.video_thread = threading.Thread(target=self.play_video, daemon=True)
                    self.video_thread.start()
            
            self.is_playing = True
            self.is_paused = False
            self.play_pause_btn.config(text="Pause")
            
            # Start progress update thread
            if not hasattr(self, 'progress_thread') or not self.progress_thread.is_alive():
                self.progress_thread = threading.Thread(target=self.update_progress, daemon=True)
                self.progress_thread.start()
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not play file: {str(e)}")
    
    def pause(self):
        """Pause media playback"""
        if self.file_type == 'audio':
            pygame.mixer.music.pause()
        
        self.is_playing = False
        self.is_paused = True
        self.play_pause_btn.config(text="Play")
    
    def stop(self):
        """Stop media playback"""
        if self.file_type == 'audio':
            pygame.mixer.music.stop()
        elif self.file_type == 'video' and self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
        self.progress_var.set(0)
        self.play_pause_btn.config(text="Play")
        
        if self.file_type == 'audio':
            self.video_label.config(text=f"♪ Audio File ♪\n{os.path.basename(self.current_file)}")
    
    def play_video(self):
        """Video playback thread"""
        fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1.0 / fps if fps > 0 else 0.033  # Default to ~30fps
        
        while self.is_playing and self.video_cap and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            
            if not ret:
                self.stop()
                break
            
            # Resize frame to fit display
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to tkinter format
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            
            # Update video display
            self.video_label.config(image=photo, text="")
            self.video_label.image = photo  # Keep a reference
            
            time.sleep(frame_delay)
    
    def update_progress(self):
        """Update progress bar and time display"""
        while self.is_playing:
            if self.file_type == 'audio':
                # For audio, we need to track time manually
                self.current_position += 1
            elif self.file_type == 'video' and self.video_cap:
                # Get current frame position
                current_frame = self.video_cap.get(cv2.CAP_PROP_POS_FRAMES)
                fps = self.video_cap.get(cv2.CAP_PROP_FPS)
                self.current_position = current_frame / fps if fps > 0 else 0
            
            # Update progress bar
            if self.duration > 0:
                progress = (self.current_position / self.duration) * 100
                self.progress_var.set(progress)
            
            # Update time display
            current_time = self.format_time(self.current_position)
            total_time = self.format_time(self.duration)
            self.time_label.config(text=f"{current_time} / {total_time}")
            
            time.sleep(1)
    
    def format_time(self, seconds):
        """Format time in MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def on_progress_change(self, value):
        """Handle progress bar changes"""
        # This would be used for seeking (more complex to implement)
        pass
    
    def on_volume_change(self, value):
        """Handle volume changes"""
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)

def main():
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()