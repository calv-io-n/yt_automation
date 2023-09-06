#!/usr/bin/python3

import os
import random
from moviepy.editor import *
from uploader import upload_to_drive as upload_video
from PIL import Image as PILImage

def resize_image_to_fit_video(img, video_size):
    img_aspect = img.width / img.height
    video_width, video_height = video_size
    
    if (video_width / video_height) > img_aspect:
        new_height = video_height
        new_width = int(new_height * img_aspect)
    else:
        new_width = video_width
        new_height = int(new_width / img_aspect)
    
    return img.resize((new_width, new_height), PILImage.LANCZOS)

def overlay_image_and_sound_on_video(video, image_path, sound_path, start_time):
    audio = AudioFileClip(sound_path)
    audio_duration = audio.duration
    
    with PILImage.open(image_path) as img:
        img = resize_image_to_fit_video(img, video.size)
        img.save("temp_resized_image.png")

    img_clip = ImageClip("temp_resized_image.png", duration=audio_duration).set_position('center').set_audio(audio)

    return CompositeVideoClip([video, img_clip.set_start(start_time).crossfadein(0.5)])

def process_video_with_multiple_sounds(video_path, image_path, audio_files, silent_audio_path):
    audio_clips = [AudioFileClip(f) for f in audio_files]
    silent_clip = AudioFileClip(silent_audio_path)

    combined_audio = []

    for audio in audio_clips:
        print(f"Audio Shape: {audio.to_soundarray().shape}")  # print the shape of each audio clip
        combined_audio.append(audio)
        combined_audio.append(silent_clip)

    combined_audio_path = "combined_audio.mp3"
    concatenate_audioclips(combined_audio[:-1]).write_audiofile(combined_audio_path)  # Excluding the last silent clip
    process_video(video_path, image_path, combined_audio_path, start_time=1)

def process_video(video_path, image_path, sound_path, start_time):
    video = VideoFileClip(video_path)
    video = overlay_image_and_sound_on_video(video, image_path, sound_path, start_time)
    video.write_videofile("output.mp4")

if __name__ == "__main__":
    subfolder_path = "./util/input/starters"
    image_path = "./util/input/reddit_posts/t1_jt9toms.png"

    print("Processing video...")
    
    mp4_files = [f for f in os.listdir(subfolder_path) if f.endswith('.mp4')]
    if not mp4_files:
        print("No MP4 files found in the subfolder!")
        exit()

    random_video = random.choice(mp4_files)
    video_path = os.path.join(subfolder_path, random_video)
    
    audio_files = [
        "./util/input/reddit_posts/test1.mp3",
        "./util/input/reddit_posts/test2.mp3",
        # Add more paths as needed
    ]

    silent_audio_path = "./util/input/silent.mp3"

    process_video_with_multiple_sounds(video_path, image_path, audio_files, silent_audio_path)
    upload_video("output.mp4")

    # Cleanup
    os.remove("temp_resized_image.png")
    os.remove("combined_audio.mp3")
