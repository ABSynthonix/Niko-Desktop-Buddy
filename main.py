import os
import sys
import tkinter as tk
import pygame
import random
from PIL import Image, ImageTk, ImageSequence


class DesktopPet:
    def __init__(self):
        pygame.mixer.init()
        full_path = self.resource_path("music.mp3")
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(0.5)
        self.playing = True

        self.root = tk.Tk()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="black")
        self.root.wm_attributes("-transparentcolor", "black")

        self.speak_timer = None

        self.user = os.getlogin()
        self.username = self.user if self.user != "guyen" else "Endie"
        self.SENTENCES = (
            f"Oh! Did you need something, {self.username}?",
            "It's a bit bright out here... but I like it!",
            "Do you think there are any pancakes here?",
            "I'll try my best! I hope you're doing okay too.",
            "It’s nice to see you again.",
            "Wait, can you see me right now?",
            "Everything looks so... digital here.",
            f"I’m glad I’m with you, {self.username}.",
            "Are we going on another quest today?",
            "I'd really like some pancakes right now..."
        )

        self.TEXT_SPACE = 200
        self.SIZES = {
            "sit": (200, 200),
            "stand": (250, 250)
        }
        self.SIZE_OFFSETS = {
            "sit": (-25, 0),
            "stand": (0, 0)
        }

        self.current_state = "sit"
        self.animations = {
            "sit": self.load_gif(self.resource_path("sit.gif")),
            "stand": self.load_gif(self.resource_path("stand.gif"))
        }

        self.frames = self.animations[self.current_state]
        self.num_frames = len(self.frames)
        self.current_frame = 0

        total_width = self.SIZES[self.current_state][0] + self.TEXT_SPACE
        self.canvas = tk.Canvas(
            self.root,
            width=total_width,
            height=self.SIZES[self.current_state][1],
            bg="black",
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()

        self.sprite_id = self.canvas.create_image(self.TEXT_SPACE, 0, image=self.frames[0], anchor="nw")

        self.text_id = self.canvas.create_text(
            self.TEXT_SPACE - 10,
            self.SIZES[self.current_state][1] // 2,
            text="",
            fill="white",
            font=("Courier", 15, "bold"),
            width=self.TEXT_SPACE - 20,
            anchor="e",
            justify="center"
        )

        self.canvas.bind("<Button-1>", self.MouseButtonClick1)
        self.canvas.bind("<Button-3>", self.MouseButtonClick2)
        self.canvas.bind("<Button-2>", self.MouseButtonClick3)

        pygame.mixer.music.play(loops=-1)

        self.update_window_pos()
        self.animate()
        self.root.mainloop()

    def load_gif(self, file_path):
        img = Image.open(file_path)
        state_key = os.path.basename(file_path).replace(".gif", "")
        target_size = self.SIZES[state_key]

        frames = []
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")
            resized_frame = frame.resize(target_size, Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(resized_frame))
        return frames

    def speak(self, message):
        if self.speak_timer is not None:
            self.root.after_cancel(self.speak_timer)

        self.canvas.itemconfig(self.text_id, text=message)
        self.speak_timer = self.root.after(3000, self.clear_text)

    def clear_text(self):
        self.canvas.itemconfig(self.text_id, text="")
        self.speak_timer = None

    def update_window_pos(self):
        state = self.current_state
        total_width = self.SIZES[state][0] + self.TEXT_SPACE
        self.root.geometry(
            f"{total_width}x{self.SIZES[state][1]}+"
            f"{self.root.winfo_screenwidth() - total_width + self.SIZE_OFFSETS[state][0]}+"
            f"{self.root.winfo_screenheight() - self.SIZES[state][1] + self.SIZE_OFFSETS[state][1] - 48}"
        )

    def MouseButtonClick2(self, event):
        self.speak(self.SENTENCES[random.randint(0, len(self.SENTENCES) - 1)])

    def MouseButtonClick1(self, event):
        new_state = "stand" if self.current_state == "sit" else "sit"
        self.current_state = new_state
        self.frames = self.animations[new_state]
        self.current_frame = 0
        self.num_frames = len(self.frames)

        new_total_width = self.SIZES[new_state][0] + self.TEXT_SPACE
        self.canvas.config(width=new_total_width, height=self.SIZES[new_state][1])

        self.canvas.coords(self.sprite_id, self.TEXT_SPACE, 0)
        self.canvas.itemconfig(self.sprite_id, image=self.frames[0])

        self.canvas.coords(self.text_id, self.TEXT_SPACE, self.SIZES[new_state][1] // 2)

        self.root.update_idletasks()
        self.update_window_pos()

    def MouseButtonClick3(self, event):
        self.playing = not self.playing
        if self.playing:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def animate(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.canvas.itemconfig(self.sprite_id, image=self.frames[self.current_frame])
        self.root.after(250, self.animate)


try:
    print("Assistant Started!")
    DesktopPet()
except KeyboardInterrupt:
    print("Assistant Closed!")