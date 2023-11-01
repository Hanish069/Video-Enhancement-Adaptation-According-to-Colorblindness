import cv2
import sys
import questionary
import numpy as np
import os
import time
from ffpyplayer.player import MediaPlayer
from pytube import YouTube
import downloadVid  # Assuming this script downloads the video

ASPECT_RATIO = 1  # Ratio of height to width for font

display_modes = [
    "YouTube",
    "Local file"
]
blindness = [
    "Protanopia",
    "Deuteranopia",
    "Tritanopia"
] 
display_choice = questionary.select(
    "Would you like to play a video from YouTube or a local file ?",
    choices=display_modes
).ask()
blindness_choice=questionary.select(
    "What is your blindness type?",
    choices=blindness
).ask()
flag=0
path = None
if display_choice == display_modes[0]:
    # Input video url
    video_url = input("Enter the YouTube video URL: ")
    save_directory = input("Enter the directory where you want to save the video: ")
  
    # Downloads video, returns path to file
    path = downloadVid.download_video(video_url,save_directory)
else:
    path = input("Then what is the path to your video? ")

# Set video source
print("Video file path:", path)
video = cv2.VideoCapture(path)
player = MediaPlayer(path)


def simulate_protanopia_to_normal_color(frame):
      # Define the range for red and green colors
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([80, 80, 255])
    lower_green = np.array([0, 100, 0])
    upper_green = np.array([80, 255, 80])

    # Create masks for red and green colors
    red_mask = cv2.inRange(frame, lower_red, upper_red)
    green_mask = cv2.inRange(frame, lower_green, upper_green)

    # Replace red and green with a color like purple
    frame[red_mask > 0] = [128, 0, 128]  # Purple
    frame[green_mask > 0] = [128, 0, 128]  # Purple

    return frame

def simulate_tritanopia_to_normal(frame):
    # Create a copy of the input frame
    result_frame = frame.copy()

    # Convert blue to red
    result_frame[:, :, 2] = frame[:, :, 0]  # Set red channel to blue channel

    # Convert yellow to green
    # Yellow color is a mix of red and green, so we distribute it between them
    result_frame[:, :, 1] = (frame[:, :, 1] + frame[:, :, 0]) // 2  # Set green channel to (green + red) / 2

    return result_frame

fps = video.get(cv2.CAP_PROP_FPS)
print(f"FPS is {fps}")
if fps == 0.0:
    frame_time = 0.0333  # Fallback to 30 FPS (1/30)
else:
    frame_time = 1 / fps

audio_frame, val = player.get_frame()

while True:
    success, image = video.read()

    if success:
        # Call the function to change red to green
        if blindness_choice==blindness[0] or blindness_choice==blindness[1]:
            image = simulate_protanopia_to_normal_color(image)
        else:
            image = simulate_tritanopia_to_normal(image)
        cv2.imshow('Video', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
cv2.destroyAllWindows()
