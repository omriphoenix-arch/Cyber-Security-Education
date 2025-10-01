"""
YouTube Playlist Downloader
Enhanced version with comprehensive network diagnostics and SSL troubleshooting
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
import threading
import os
import re
import sys
import subprocess
from pathlib import Path
import ssl
import urllib3
import socket

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("750x700")
        self.root.configure(bg="#2c3e50")
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.playlist_url = tk.StringVar()
        self.format_choice = tk.StringVar(value="mp3")
        self.quality_choice = tk.StringVar(value="best")
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title_label = tk.Label(main_frame, text="� YouTube Playlist Downloader 🎬", 
                              font=("Arial", 16, "bold"), 
                              fg="#e74c3c", bg="#2c3e50")
        title_label.pack(pady=(0, 15))
        
        # Network diagnostics frame
        diag_frame = tk.LabelFrame(main_frame, text="Network Diagnostics", 
                                  font=("Arial", 11, "bold"),
                                  fg="#f39c12", bg="#34495e", bd=2)
        diag_frame.pack(fill=tk.X, pady=(0, 15))
        
        diag_buttons = tk.Frame(diag_frame, bg="#34495e")
        diag_buttons.pack(padx=10, pady=8)
        
        self.ping_btn = tk.Button(diag_buttons, text="🌐 Ping YouTube",
                                 command=self.ping_youtube,
                                 font=("Arial", 9), bg="#3498db", fg="white",
                                 relief="flat", padx=12)
        self.ping_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.dns_btn = tk.Button(diag_buttons, text="🔍 Check DNS",
                               command=self.check_dns,
                               font=("Arial", 9), bg="#9b59b6", fg="white",
                               relief="flat", padx=12)
        self.dns_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.ssl_btn = tk.Button(diag_buttons, text="🔐 Test SSL",
                               command=self.test_ssl,
                               font=("Arial", 9), bg="#e67e22", fg="white",
                               relief="flat", padx=12)
        self.ssl_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.ytdlp_btn = tk.Button(diag_buttons, text="📺 Test yt-dlp",
                                 command=self.test_ytdlp_simple,
                                 font=("Arial", 9), bg="#27ae60", fg="white",
                                 relief="flat", padx=12)
        self.ytdlp_btn.pack(side=tk.LEFT)
        
        # URL Input Frame
        url_frame = tk.LabelFrame(main_frame, text="Playlist URL", 
                                 font=("Arial", 11, "bold"),
                                 fg="#ecf0f1", bg="#34495e", bd=2)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        url_entry_frame = tk.Frame(url_frame, bg="#34495e")
        url_entry_frame.pack(fill=tk.X, padx=10, pady=8)
        
        self.url_entry = tk.Entry(url_entry_frame, textvariable=self.playlist_url,
                                 font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50",
                                 relief="flat", bd=5)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        self.analyze_btn = tk.Button(url_entry_frame, text="Analyze",
                                   command=self.analyze_playlist,
                                   font=("Arial", 9), bg="#3498db", fg="white",
                                   relief="flat", padx=12)
        self.analyze_btn.pack(side=tk.RIGHT)
        
        # Settings Frame (Compact)
        settings_frame = tk.LabelFrame(main_frame, text="Settings", 
                                     font=("Arial", 11, "bold"),
                                     fg="#ecf0f1", bg="#34495e", bd=2)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        settings_content = tk.Frame(settings_frame, bg="#34495e")
        settings_content.pack(fill=tk.X, padx=10, pady=8)
        
        # Format and quality in one row
        tk.Label(settings_content, text="Format:", font=("Arial", 9, "bold"),
                fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT)
        
        tk.Radiobutton(settings_content, text="MP3", variable=self.format_choice,
                      value="mp3", font=("Arial", 9), fg="#ecf0f1", bg="#34495e",
                      selectcolor="#2c3e50").pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Radiobutton(settings_content, text="MP4", variable=self.format_choice,
                      value="mp4", font=("Arial", 9), fg="#ecf0f1", bg="#34495e",
                      selectcolor="#2c3e50").pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(settings_content, text="Quality:", font=("Arial", 9, "bold"),
                fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT)
        
        quality_combo = ttk.Combobox(settings_content, textvariable=self.quality_choice,
                                   values=["best", "720p", "480p", "360p"],
                                   state="readonly", width=10, font=("Arial", 9))
        quality_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Download path
        path_frame = tk.Frame(settings_frame, bg="#34495e")
        path_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        tk.Label(path_frame, text="Save to:", font=("Arial", 9, "bold"),
                fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT)
        
        self.path_entry = tk.Entry(path_frame, textvariable=self.download_path,
                                  font=("Arial", 9), bg="#ecf0f1", fg="#2c3e50",
                                  relief="flat", bd=3, width=40)
        self.path_entry.pack(side=tk.LEFT, padx=(5, 8))
        
        self.browse_btn = tk.Button(path_frame, text="Browse",
                                  command=self.browse_folder,
                                  font=("Arial", 9), bg="#95a5a6", fg="white",
                                  relief="flat", padx=10)
        self.browse_btn.pack(side=tk.LEFT)
        
        # Log Frame
        log_frame = tk.LabelFrame(main_frame, text="Diagnostics & Logs", 
                                font=("Arial", 11, "bold"),
                                fg="#ecf0f1", bg="#34495e", bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=80,
                                                font=("Consolas", 8), bg="#ecf0f1",
                                                fg="#2c3e50", relief="flat")
        self.log_text.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        
        # Progress and Controls
        progress_frame = tk.Frame(main_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = tk.Label(progress_frame, text="Ready - Run diagnostics first", 
                                     font=("Arial", 9), fg="#bdc3c7", bg="#2c3e50")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(3, 0))
        
        # Control buttons
        buttons_frame = tk.Frame(main_frame, bg="#2c3e50")
        buttons_frame.pack()
        
        self.download_btn = tk.Button(buttons_frame, text="📥 Download",
                                    command=self.start_download,
                                    font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
                                    relief="flat", padx=20, pady=6, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹ Stop",
                                command=self.stop_download,
                                font=("Arial", 11, "bold"), bg="#e74c3c", fg="white",
                                relief="flat", padx=20, pady=6, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(buttons_frame, text="🗑 Clear",
                                 command=self.clear_log,
                                 font=("Arial", 11, "bold"), bg="#95a5a6", fg="white",
                                 relief="flat", padx=20, pady=6)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Initial message
        self.log_message("🚀 Network Troubleshoot YouTube Downloader Ready!")
        self.log_message("📋 Step 1: Run network diagnostics to identify issues")
        self.log_message("📋 Step 2: If diagnostics pass, paste playlist URL and analyze")
        self.log_message("📋 Step 3: Download your playlist!")
        self.log_message("")
    
    def log_message(self, message):
        """Add message to the log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("📝 Log cleared - Ready for new diagnostics")
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def ping_youtube(self):
        """Test basic connectivity to YouTube"""
        self.ping_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Pinging YouTube...")
        self.log_message("🌐 Testing basic connectivity to YouTube...")
        
        thread = threading.Thread(target=self._ping_youtube_thread)
        thread.daemon = True
        thread.start()
    
    def _ping_youtube_thread(self):
        """Ping YouTube in separate thread"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['ping', '-n', '3', 'www.youtube.com'], 
                                      capture_output=True, text=True, timeout=15)
            else:  # Linux/Mac
                result = subprocess.run(['ping', '-c', '3', 'www.youtube.com'], 
                                      capture_output=True, text=True, timeout=15)
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            self.root.after(0, self._ping_result, success, output)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self._ping_result, False, "Ping timed out after 15 seconds")
        except Exception as e:
            self.root.after(0, self._ping_result, False, str(e))
    
    def _ping_result(self, success, output):
        """Handle ping result"""
        self.ping_btn.config(state=tk.NORMAL)
        
        if success:
            self.log_message("✅ Ping successful - Basic connectivity OK")
            self.log_message(f"📊 Ping details: {output.split()[-3:-1] if output else 'Success'}")
        else:
            self.log_message("❌ Ping failed - Check internet connection")
            self.log_message(f"📊 Error: {output[:100]}...")
        
        self.progress_label.config(text="Ping test complete")
    
    def check_dns(self):
        """Check DNS resolution for YouTube"""
        self.dns_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Checking DNS...")
        self.log_message("🔍 Testing DNS resolution for YouTube...")
        
        thread = threading.Thread(target=self._check_dns_thread)
        thread.daemon = True
        thread.start()
    
    def _check_dns_thread(self):
        """Check DNS in separate thread"""
        try:
            # Try to resolve YouTube domains
            domains = ['www.youtube.com', 'youtube.com', 'googlevideo.com']
            results = []
            
            for domain in domains:
                try:
                    ip = socket.gethostbyname(domain)
                    results.append(f"✅ {domain} -> {ip}")
                except socket.gaierror as e:
                    results.append(f"❌ {domain} -> Failed: {e}")
            
            self.root.after(0, self._dns_result, True, results)
            
        except Exception as e:
            self.root.after(0, self._dns_result, False, [str(e)])
    
    def _dns_result(self, success, results):
        """Handle DNS result"""
        self.dns_btn.config(state=tk.NORMAL)
        
        if success:
            self.log_message("🔍 DNS resolution test results:")
            for result in results:
                self.log_message(f"   {result}")
            
            failed_count = sum(1 for r in results if '❌' in r)
            if failed_count == 0:
                self.log_message("✅ All DNS lookups successful")
            else:
                self.log_message(f"⚠️ {failed_count} DNS lookups failed")
        else:
            self.log_message("❌ DNS test failed completely")
            for result in results:
                self.log_message(f"   {result}")
        
        self.progress_label.config(text="DNS test complete")
    
    def test_ssl(self):
        """Test SSL connection to YouTube"""
        self.ssl_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Testing SSL...")
        self.log_message("🔐 Testing SSL connection to YouTube...")
        
        thread = threading.Thread(target=self._test_ssl_thread)
        thread.daemon = True
        thread.start()
    
    def _test_ssl_thread(self):
        """Test SSL in separate thread"""
        try:
            import ssl
            import socket
            
            # Test different SSL configurations
            contexts = [
                ("Default SSL", ssl.create_default_context()),
                ("Insecure SSL", ssl._create_unverified_context()),
            ]
            
            results = []
            
            for name, context in contexts:
                try:
                    with socket.create_connection(('www.youtube.com', 443), timeout=10) as sock:
                        with context.wrap_socket(sock, server_hostname='www.youtube.com') as ssock:
                            version = ssock.version()
                            cipher = ssock.cipher()
                            results.append(f"✅ {name}: {version}, Cipher: {cipher[0] if cipher else 'Unknown'}")
                except Exception as e:
                    results.append(f"❌ {name}: {str(e)[:50]}...")
            
            self.root.after(0, self._ssl_result, results)
            
        except Exception as e:
            self.root.after(0, self._ssl_result, [f"❌ SSL test failed: {str(e)}"])
    
    def _ssl_result(self, results):
        """Handle SSL test result"""
        self.ssl_btn.config(state=tk.NORMAL)
        
        self.log_message("🔐 SSL connection test results:")
        for result in results:
            self.log_message(f"   {result}")
        
        success_count = sum(1 for r in results if '✅' in r)
        if success_count > 0:
            self.log_message(f"✅ {success_count} SSL method(s) working")
        else:
            self.log_message("❌ All SSL methods failed - this may cause download issues")
        
        self.progress_label.config(text="SSL test complete")
    
    def test_ytdlp_simple(self):
        """Test yt-dlp with a simple video"""
        self.ytdlp_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Testing yt-dlp...")
        self.log_message("📺 Testing yt-dlp with simple video...")
        
        thread = threading.Thread(target=self._test_ytdlp_thread)
        thread.daemon = True
        thread.start()
    
    def _test_ytdlp_thread(self):
        """Test yt-dlp in separate thread"""
        try:
            # Use a very simple, short video for testing
            test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
            
            # Try multiple configurations
            configs = [
                {
                    'name': 'Basic',
                    'opts': {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'socket_timeout': 30,
                    }
                },
                {
                    'name': 'Legacy SSL',
                    'opts': {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'legacy_server_connect': True,
                        'nocheckcertificate': True,
                        'socket_timeout': 30,
                    }
                },
                {
                    'name': 'Alternative Client',
                    'opts': {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android'],
                            }
                        },
                        'socket_timeout': 30,
                    }
                }
            ]
            
            results = []
            working_config = None
            
            for config in configs:
                try:
                    with yt_dlp.YoutubeDL(config['opts']) as ydl:
                        info = ydl.extract_info(test_url, download=False)
                        title = info.get('title', 'Test Video')
                        results.append(f"✅ {config['name']}: Retrieved '{title[:30]}...'")
                        if not working_config:
                            working_config = config
                        break  # Stop on first success
                except Exception as e:
                    error_msg = str(e)[:60] + "..." if len(str(e)) > 60 else str(e)
                    results.append(f"❌ {config['name']}: {error_msg}")
            
            self.root.after(0, self._ytdlp_result, results, working_config)
            
        except Exception as e:
            self.root.after(0, self._ytdlp_result, [f"❌ yt-dlp test failed: {str(e)}"], None)
    
    def _ytdlp_result(self, results, working_config):
        """Handle yt-dlp test result"""
        self.ytdlp_btn.config(state=tk.NORMAL)
        
        self.log_message("📺 yt-dlp test results:")
        for result in results:
            self.log_message(f"   {result}")
        
        if working_config:
            self.log_message(f"✅ Working configuration found: {working_config['name']}")
            self.log_message("🎉 You should be able to download playlists now!")
            self.working_ytdlp_config = working_config['opts']
        else:
            self.log_message("❌ No yt-dlp configuration worked")
            self.log_message("💡 Try using a VPN or different network")
            self.working_ytdlp_config = None
        
        self.progress_label.config(text="yt-dlp test complete")
    
    def get_optimal_options(self):
        """Get optimal yt-dlp options based on tests"""
        if hasattr(self, 'working_ytdlp_config') and self.working_ytdlp_config:
            return self.working_ytdlp_config.copy()
        else:
            # Fallback configuration
            return {
                'legacy_server_connect': True,
                'nocheckcertificate': True,
                'socket_timeout': 60,
                'retries': 5,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                }
            }
    
    def analyze_playlist(self):
        """Analyze playlist with optimal settings"""
        url = self.playlist_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL")
            return
        
        self.analyze_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Analyzing playlist...")
        self.progress_bar.start()
        self.log_message(f"🔍 Analyzing: {url}")
        
        thread = threading.Thread(target=self._analyze_playlist_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _analyze_playlist_thread(self, url):
        """Analyze playlist in separate thread"""
        try:
            ydl_opts = self.get_optimal_options()
            ydl_opts.update({
                'extract_flat': True,
                'playlist_items': '1:10',  # Just first 10 for analysis
            })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.root.after(0, self._analyze_success, info)
                
        except Exception as e:
            self.root.after(0, self._analyze_error, str(e))
    
    def _analyze_success(self, info):
        """Handle successful analysis"""
        self.progress_bar.stop()
        self.analyze_btn.config(state=tk.NORMAL)
        
        if 'entries' in info:
            title = info.get('title', 'Unknown Playlist')
            count = len(info['entries'])
            
            self.log_message(f"✅ Found playlist: {title}")
            self.log_message(f"📊 Video count: {count}")
            self.log_message("🎯 Ready to download!")
            
            self.download_btn.config(state=tk.NORMAL)
        else:
            self.log_message("⚠️ This appears to be a single video, not a playlist")
        
        self.progress_label.config(text="Analysis complete")
    
    def _analyze_error(self, error):
        """Handle analysis error"""
        self.progress_bar.stop()
        self.analyze_btn.config(state=tk.NORMAL)
        
        self.log_message(f"❌ Analysis failed: {error[:100]}...")
        self.log_message("💡 Try running diagnostics first to identify the issue")
        
        self.progress_label.config(text="Analysis failed")
    
    def start_download(self):
        """Start download with optimal settings"""
        if self.is_downloading:
            return
        
        url = self.playlist_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL")
            return
        
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.log_message("🚀 Starting download with optimal settings...")
        
        thread = threading.Thread(target=self._download_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url):
        """Download in separate thread"""
        try:
            ydl_opts = self.get_optimal_options()
            
            if self.format_choice.get() == "mp3":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                quality = self.quality_choice.get()
                if quality == "best":
                    format_str = 'best[ext=mp4]'
                else:
                    format_str = f'best[height<={quality[:-1]}][ext=mp4]'
                
                ydl_opts.update({
                    'format': format_str,
                    'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.root.after(0, self._download_complete, True, "Download completed!")
            
        except Exception as e:
            self.root.after(0, self._download_complete, False, str(e))
    
    def _download_complete(self, success, message):
        """Handle download completion"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        
        if success:
            self.log_message("🎉 " + message)
            messagebox.showinfo("Success", message)
        else:
            self.log_message("❌ " + message[:100] + "...")
            messagebox.showerror("Error", "Download failed. Check logs for details.")
        
        self.progress_label.config(text="Download complete")
    
    def stop_download(self):
        """Stop download"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self.log_message("⏹ Download stopped")
        self.progress_label.config(text="Download stopped")

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()