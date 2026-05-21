import customtkinter as ctk
from PIL import Image
import math
import colorsys

class ColorWheel(ctk.CTkLabel):
    def __init__(self, master, size=200, command=None, **kwargs):
        self.size = size
        self.command = command
        self.wheel_image = self.generate_wheel_image(size)
        self.ctk_image = ctk.CTkImage(light_image=self.wheel_image, dark_image=self.wheel_image, size=(size, size))
        
        super().__init__(master, text="", image=self.ctk_image, **kwargs)
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_click)

    def generate_wheel_image(self, size):
        image = Image.new("RGBA", (size, size), (0,0,0,0))
        pixels = image.load()
        center = size / 2
        radius = size / 2
        for x in range(size):
            for y in range(size):
                dx = x - center
                dy = y - center
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= radius:
                    angle = math.atan2(dy, dx)
                    hue = (angle / (2 * math.pi)) % 1.0
                    sat = distance / radius
                    r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
                    pixels[x, y] = (int(r*255), int(g*255), int(b*255), 255)
        return image

    def on_click(self, event):
        x, y = event.x, event.y
        center = self.size / 2
        dx = x - center
        dy = y - center
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > center:
            angle = math.atan2(dy, dx)
            distance = center
        else:
            angle = math.atan2(dy, dx)
            
        hue = (angle / (2 * math.pi)) % 1.0
        sat = distance / center
        r, g, b = colorsys.hsv_to_rgb(hue, sat, 1.0)
        
        hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        if self.command:
            self.command(hex_color)
