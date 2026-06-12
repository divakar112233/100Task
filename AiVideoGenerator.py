from gtts import gTTS
from moviepy import *
from PIL import Image, ImageDraw, ImageFont

# Text for video
text = input("Enter text for video: ")

# Generate AI voice
tts = gTTS(text=text, lang='en')
tts.save("voice.mp3")

# Create image
img = Image.new('RGB', (1280, 720), color='black')
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 50)
except:
    font = ImageFont.load_default()

draw.text((100, 300), text, fill="white", font=font)

img.save("frame.png")

# Create video
audio = AudioFileClip("voice.mp3")
video = ImageClip("frame.png").with_duration(audio.duration)
video = video.with_audio(audio)

video.write_videofile("ai_video.mp4", fps=24)

print("AI Video Generated Successfully!")