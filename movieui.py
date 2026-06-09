import customtkinter as ctk
from PIL import Image, ImageTk
import os
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GrokMusic(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Grok Music")
        self.geometry("1280x720")
        self.minsize(1100, 650)
        
        # Variables
        self.current_song = 0
        self.is_playing = False
        self.songs = [
            {"title": "Midnight Drive", "artist": "Neon Waves", "duration": "3:42"},
            {"title": "Echoes", "artist": "Luna Collective", "duration": "4:15"},
            {"title": "Digital Heart", "artist": "Void", "duration": "2:58"},
            {"title": "Starlight", "artist": "Aether", "duration": "3:29"},
            {"title": "Afterglow", "artist": "Solaris", "duration": "4:03"},
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ================= SIDEBAR =================
        sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#0f172a")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        
        # Logo
        logo = ctk.CTkLabel(sidebar, text="GROK", font=ctk.CTkFont("Arial", 42, "bold"), text_color="#22d3ee")
        logo.pack(pady=(30, 0))
        ctk.CTkLabel(sidebar, text="MUSIC", font=ctk.CTkFont("Arial", 18), text_color="gray").pack(pady=(0, 40))
        
        # Nav
        nav_items = ["Home", "Discover", "Library"]
        for item in nav_items:
            btn = ctk.CTkButton(sidebar, text=item, height=45, fg_color="transparent", 
                              anchor="w", font=ctk.CTkFont(size=16), hover_color="#1e2937")
            btn.pack(pady=4, padx=20, fill="x")
        
        # Playlists
        ctk.CTkLabel(sidebar, text="Playlists", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=30, pady=(30,10))
        playlists = ["Daily Drive", "Chill Hits", "Neon Nights", "Focus Flow", "Desi Beats", "Workout"]
        for pl in playlists:
            ctk.CTkButton(sidebar, text=pl, height=35, fg_color="transparent", 
                         text_color="gray", hover_color="#1e2937", anchor="w").pack(pady=2, padx=30, fill="x")
        
        # ================= MAIN CONTENT =================
        main = ctk.CTkFrame(self, fg_color="#0f172a")
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(main, text="Good evening, Da 🔥", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", pady=(0,20))
        
        # Now Playing Card
        now_frame = ctk.CTkFrame(main, fg_color="#1e2937", corner_radius=20, height=420)
        now_frame.pack(fill="x", pady=10)
        now_frame.pack_propagate(False)
        
        # Album Art
        art_frame = ctk.CTkFrame(now_frame, fg_color="#334155", width=320, height=320, corner_radius=15)
        art_frame.place(x=50, y=50)
        
        # Fake Album Cover
        label = ctk.CTkLabel(art_frame, text="♪", font=ctk.CTkFont(size=140), text_color="#64748b")
        label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Song Info
        song = self.songs[self.current_song]
        self.song_title = ctk.CTkLabel(now_frame, text=song["title"], font=ctk.CTkFont(size=26, weight="bold"))
        self.song_title.place(x=430, y=100)
        
        self.song_artist = ctk.CTkLabel(now_frame, text=song["artist"], font=ctk.CTkFont(size=18), text_color="gray")
        self.song_artist.place(x=430, y=150)
        
        # Progress
        self.progress = ctk.CTkSlider(now_frame, from_=0, to=100, width=500, height=6, 
                                    button_color="#22d3ee", button_hover_color="#67e8f9")
        self.progress.set(35)
        self.progress.place(x=430, y=230)
        
        ctk.CTkLabel(now_frame, text="1:24", text_color="gray").place(x=430, y=260)
        ctk.CTkLabel(now_frame, text=song["duration"], text_color="gray").place(x=880, y=260)
        
        # Controls
        controls = ctk.CTkFrame(now_frame, fg_color="transparent")
        controls.place(x=430, y=310)
        
        ctk.CTkButton(controls, text="⏮", width=60, height=60, font=ctk.CTkFont(size=24),
                     fg_color="transparent", hover_color="#334155", command=self.prev_song).pack(side="left", padx=10)
        
        self.play_btn = ctk.CTkButton(controls, text="▶", width=80, height=80, font=ctk.CTkFont(size=32),
                                    fg_color="#22d3ee", text_color="black", hover_color="#67e8f9",
                                    corner_radius=50, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=15)
        
        ctk.CTkButton(controls, text="⏭", width=60, height=60, font=ctk.CTkFont(size=24),
                     fg_color="transparent", hover_color="#334155", command=self.next_song).pack(side="left", padx=10)
        
        # Song List
        list_frame = ctk.CTkScrollableFrame(main, fg_color="transparent", height=200)
        list_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(list_frame, text="Queue", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0,10))
        
        for i, song in enumerate(self.songs):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=f"{i+1}. {song['title']}", font=ctk.CTkFont(size=15)).pack(side="left")
            ctk.CTkLabel(row, text=song["artist"], text_color="gray").pack(side="left", padx=20)
            ctk.CTkLabel(row, text=song["duration"], text_color="gray").pack(side="right")

    def toggle_play(self):
        self.is_playing = not self.is_playing
        self.play_btn.configure(text="⏸" if self.is_playing else "▶")

    def next_song(self):
        self.current_song = (self.current_song + 1) % len(self.songs)
        self.update_song()

    def prev_song(self):
        self.current_song = (self.current_song - 1) % len(self.songs)
        self.update_song()

    def update_song(self):
        song = self.songs[self.current_song]
        self.song_title.configure(text=song["title"])
        self.song_artist.configure(text=song["artist"])

if __name__ == "__main__":
    app = GrokMusic()
    app.mainloop()