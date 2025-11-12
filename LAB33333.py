import tkinter as tk
import random
import string
import winsound
import os
from PIL import Image, ImageTk


WIDTH = 800
HEIGHT = 600

class KeyGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Key Generator v2.0")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        
        self.music_playing = False
        self.music_file_path = self.find_music_file()
        self.bg_image = None
        
        self.setup_ui()
        
        self.root.after(500, self.auto_generate)
        
        self.root.after(1000, self.toggle_music)
    
    def setup_ui(self):
        """Setup user interface"""
        self.setup_background()
        
        self.main_frame = tk.Frame(
            self.root, 
            bg="#2c3e50", 
            relief=tk.RAISED, 
            bd=2
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=650, height=400)
        
        self.create_widgets()
    
    def setup_background(self):
        """Setup background image"""
        image_paths = [
            r"D:\USER\ONEDRIVE\桌面\Python\bg_image.png.jpg"
        ]
        
        for path in image_paths:
            if os.path.exists(path):
                try:
                    pil_image = Image.open(path)
                    pil_image = pil_image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                    self.bg_image = ImageTk.PhotoImage(pil_image)
                    
                    bg_label = tk.Label(self.root, image=self.bg_image)
                    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                    bg_label.image = self.bg_image
                    return
                except Exception as e:
                    continue
        
        self.root.configure(bg="#2c3e50")
    
    def create_widgets(self):
        """Create interface widgets"""
        title_label = tk.Label(
            self.main_frame,
            text="Advanced Key Generator",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=10
        )
        title_label.pack(pady=20)
        
        self.btn_generate = tk.Button(
            self.main_frame, 
            text="Generate New Key", 
            font=("Arial", 14), 
            bg="#3498db", 
            fg="white",
            bd=2,
            relief=tk.RAISED,
            command=self.generate_key,
            width=15,
            cursor="hand2"
        )
        self.btn_generate.pack(pady=15)
        
        self.entry_key = tk.Entry(
            self.main_frame,
            font=("Arial", 16, "bold"),
            bg="#ecf0f1",
            fg="#e74c3c",
            justify=tk.CENTER,
            width=35,
            bd=3,
            relief=tk.GROOVE
        )
        self.entry_key.pack(pady=20)
        self.entry_key.config(state=tk.DISABLED)
        
        music_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        music_frame.pack(pady=10)
        
        self.btn_music = tk.Button(
            music_frame,
            text="🔇 Music Off",
            font=("Arial", 10),
            bg="#9b59b6",
            fg="white",
            bd=1,
            relief=tk.RAISED,
            command=self.toggle_music,
            width=12
        )
        self.btn_music.pack()
        
        self.status_text = tk.StringVar()
        self.status_text.set("Ready")
        
        status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_text,
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        status_label.pack(pady=5)
        
        info_label = tk.Label(
            self.main_frame,
            text="Format: XXXX-XXXX-XXXX | Each block weight sum: 30-35",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        info_label.pack(pady=5)
    
    def get_char_weight(self, c):
        """Calculate character weight"""
        if c.isalpha():
            return ord(c) - ord('A') + 1
        else:
            return int(c)
    
    def generate_valid_block(self):
        """Generate valid block with weight 30-35"""
        chars = string.ascii_uppercase + string.digits
        while True:
            block = random.sample(chars, 4)
            total_weight = sum(self.get_char_weight(c) for c in block)
            if 30 <= total_weight <= 35:
                return ''.join(block)
    
    def play_sound(self, sound_type):
        """Play sound effects"""
        try:
            if sound_type == "click":
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            elif sound_type == "success":
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            elif sound_type == "typewriter":
                winsound.Beep(random.randint(300, 600), 30)
            elif sound_type == "generating":
                frequencies = [523, 587, 659, 698, 784, 880, 988, 1047]
                winsound.Beep(random.choice(frequencies), 80)
        except:
 
            if sound_type == "click":
                winsound.Beep(800, 100)
            elif sound_type == "success":
                winsound.Beep(1000, 200)
            
    
    def generate_key(self):
        """Generate key with animation"""
        self.play_sound("click")
        
        self.btn_generate.config(bg="#2980b9", state=tk.DISABLED)
        
        self.entry_key.config(state=tk.NORMAL, fg="#3498db")
        self.entry_key.delete(0, tk.END)
        self.entry_key.insert(0, "Generating...")
        
        self.play_sound("generating")
        
        self.root.after(1500, self.finish_generation)
    
    def finish_generation(self):
        """Finish key generation"""
        key_blocks = []
        for i in range(3):
            key_blocks.append(self.generate_valid_block())
        
        final_key = '-'.join(key_blocks)
        
        self.entry_key.delete(0, tk.END)
        self.entry_key.insert(0, final_key)
        self.entry_key.config(state=tk.DISABLED, fg="#e74c3c")
        
        self.play_sound("success")
        
        self.btn_generate.config(bg="#3498db", state=tk.NORMAL)
        
        self.status_text.set("Key generated successfully!")
        self.root.after(2000, lambda: self.status_text.set("Ready"))
    
    def auto_generate(self):
        """Auto generate key on startup"""
        self.finish_generation()
    
    def find_music_file(self):
        """Find music file"""
        music_paths = [
            r"D:\USER\ONEDRIVE\桌面\Python\8bit.wav"
        ]
        
        for path in music_paths:
            if os.path.exists(path):
                return path
        return None
    
    def play_background_music(self):
        """Play background music in loop"""
        if self.music_playing and self.music_file_path:
            try:
                winsound.PlaySound(self.music_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                self.root.after(30000, self.play_background_music)
            except:
                self.root.after(1000, self.play_system_music)
        elif self.music_playing:
            self.play_system_music()
    
    def play_system_music(self):
        """Play system music as fallback"""
        if self.music_playing:

            melody = [523, 659, 784, 880, 784, 659, 523]
            for freq in melody:
                if self.music_playing:
                    winsound.Beep(freq, 300)
                else:
                    break
          
            if self.music_playing:
                self.root.after(5000, self.play_system_music)
    
    def toggle_music(self):
        """Toggle background music"""
        self.music_playing = not self.music_playing
        
        if self.music_playing:
            self.btn_music.config(text="🔊 Music On")
            self.play_background_music()
        else:
            self.btn_music.config(text="🔇 Music Off")

            winsound.PlaySound(None, winsound.SND_PURGE)
     
    
    def run(self):
        """Run application"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyGenerator()
    app.run()