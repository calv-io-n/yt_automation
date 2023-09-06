import sys
import os

sys.path.append("..") 
from downloader import download_video
from crop_starter import crop_to_vertical
from uploader import upload_to_drive  # Here's the change

def input_short(url):
    print("Downloading video...")
    downloaded_path = download_video(url)

    print("Cropping video...")
    cropped_path = crop_to_vertical(downloaded_path)

    # Delete the video at downloaded_path after cropping
    print("Deleting video...")
    os.remove(downloaded_path)

    return cropped_path

if __name__ == "__main__":
    path = input_short('https://www.youtube.com/watch?v=dCiwaWF9Iro')

    print("Uploading video...")
    upload_to_drive(path)  # Here's the change
    print(f"Video downloaded to: {path}")
