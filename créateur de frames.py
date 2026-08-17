from PIL import Image
import os

gif = Image.open("loading-6.gif")
frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.copy()
    frame.save(f"frame_{i}.png")
    frames.append(f"frame_{i}.png")

print("Images extraites du GIF !")
