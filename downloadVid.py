import os
from pytube import YouTube

def download_video(video_url, save_directory):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream (you can choose a different stream if needed)
        stream = yt.streams.get_highest_resolution()

        # Get the video title to use as the filename
        video_title = yt.title

        # Combine the save directory and the video title to create the full file path
        file_path = os.path.join(save_directory, video_title)

        # Download the video to the specified path
        stream.download(output_path=save_directory, filename=video_title)

        print(f"Video downloaded to {file_path}")
        return file_path
    except Exception as e:
        print(f"An error occurred while downloading the video: {str(e)}")
