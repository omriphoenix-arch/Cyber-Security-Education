#!/usr/bin/env python3
"""
Fake Virus Launcher - Educational Demo

Simple launcher for educational "fake virus" demonstrations.
All tools are harmless and for cybersecurity education only.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class FakeVirusLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⚠️ Fake Virus Demo Launcher - EDUCATIONAL ONLY")
        self.root.geometry("500x400")
        self.root.configure(bg='black')
        
        # Make it look "scary" but clearly educational
        self.setup_gui()
    
    def setup_gui(self):
        # Warning header
        warning_label = tk.Label(self.root, 
                               text="⚠️ EDUCATIONAL MALWARE SIMULATOR ⚠️",
                               font=('Courier New', 14, 'bold'),
                               fg='red', bg='black')
        warning_label.pack(pady=10)
        
        # Disclaimer
        disclaimer = tk.Label(self.root,
                            text="These are HARMLESS educational demonstrations\nNo actual viruses or malware!",
                            font=('Arial', 10),
                            fg='yellow', bg='black')
        disclaimer.pack(pady=5)
        
        # Separator
        separator = tk.Label(self.root, text="═" * 50, fg='green', bg='black')
        separator.pack(pady=10)
        
        # Demo buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=20, expand=True)
        
        demos = [
            ("🎬 Hollywood Hacker Screen", self.launch_hollywood_screen, "Movie-style 'hacking' display"),
            ("🦠 Fake Virus Scanner", self.fake_virus_scanner, "Pretend antivirus detection"),
            ("💀 Scary Warning Messages", self.scary_warnings, "Harmless popup demonstrations"),
            ("🔒 Fake Ransomware Screen", self.fake_ransomware, "Educational ransomware simulation")
        ]
        
        for name, command, description in demos:
            btn = tk.Button(button_frame,
                          text=name,
                          command=command,
                          font=('Arial', 11, 'bold'),
                          bg='darkred',
                          fg='white',
                          width=25,
                          height=2)
            btn.pack(pady=5)
            
            desc_label = tk.Label(button_frame,
                                text=description,
                                font=('Arial', 8),
                                fg='gray', bg='black')
            desc_label.pack()
        
        # Exit button
        exit_btn = tk.Button(self.root,
                           text="EXIT SAFELY",
                           command=self.root.quit,
                           font=('Arial', 12, 'bold'),
                           bg='green',
                           fg='white',
                           width=15)
        exit_btn.pack(pady=20)
        
        # Educational note
        edu_note = tk.Label(self.root,
                          text="Remember: Real malware is dangerous!\nThis is for education and awareness only.",
                          font=('Arial', 9),
                          fg='cyan', bg='black')
        edu_note.pack(pady=10)
    
    def launch_hollywood_screen(self):
        """Launch the Hollywood hacker screen"""
        try:
            subprocess.Popen([sys.executable, 'hollywood_hacker_screen.py'])
            messagebox.showinfo("Demo Started", "Hollywood Hacker Screen launched!\nPress ESC or F11 to exit fullscreen.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch demo: {e}")
    
    def fake_virus_scanner(self):
        """Show fake virus scanner popup"""
        messagebox.showwarning("🦠 FAKE ANTIVIRUS ALERT", 
                             "VIRUS DETECTED!\n\n" +
                             "Trojan.Generic.FakeDemo\n" +
                             "Location: C:\\FakeVirus\\demo.exe\n" +
                             "Threat Level: EDUCATIONAL\n\n" +
                             "This is a FAKE alert for demonstration purposes!\n" +
                             "No actual viruses are present.")
    
    def scary_warnings(self):
        """Show series of fake scary warnings"""
        warnings = [
            "⚠️ SYSTEM COMPROMISE DETECTED!",
            "🔥 ALL YOUR FILES ARE BELONG TO US!",
            "💀 YOUR COMPUTER HAS BEEN HACKED!",
            "🚨 JUST KIDDING! This is educational! 😄"
        ]
        
        for warning in warnings:
            messagebox.showwarning("Fake Warning", warning)
    
    def fake_ransomware(self):
        """Show fake ransomware message"""
        messagebox.showerror("🔒 FAKE RANSOMWARE ALERT", 
                           "YOUR FILES HAVE BEEN ENCRYPTED!\n\n" +
                           "Send 100 Bitcoin to: 1FakeAddress123\n" +
                           "To decrypt your files...\n\n" +
                           "JUST KIDDING! 😂\n" +
                           "This is an educational demonstration!\n" +
                           "Your files are perfectly safe.\n\n" +
                           "Real ransomware is a serious threat - always:\n" +
                           "• Keep backups\n" +
                           "• Update software\n" +
                           "• Use antivirus\n" +
                           "• Be cautious with emails")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Fake Virus Educational Launcher...")
    app = FakeVirusLauncher()
    app.run()