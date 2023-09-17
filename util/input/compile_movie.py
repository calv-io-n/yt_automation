#!/usr/bin/python3

import os
import random
from moviepy.editor import *
from uploader import upload_to_drive as upload_video
from PIL import Image as PILImage
from moviepy.video.VideoClip import ColorClip
from captions import create_caption, split_text_into_lines, transcribe_audio_with_whisper, save_to_json, load_from_json

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

def image_and_sound_to_video(image_path, sound_path, video_size, video_enabled=True, POST_TYPE="askReddit"):
    """Convert image and sound to a video clip."""
    print(sound_path)

    audio = AudioFileClip(sound_path)
    audio_duration = audio.duration
    
    if not video_enabled:
        blank_clip = ColorClip(video_size, color=(0,0,0), duration=audio_duration).set_opacity(0)

        transcription_result = transcribe_audio_with_whisper(sound_path)
        wordlevel_info = []
        for segment in transcription_result['segments']:
            for word in segment['words']:
                wordlevel_info.append({'word': word['word'].strip(), 'start': word['start'], 'end': word['end']}) 
        save_to_json(wordlevel_info, "data.json")
        wordlevel_info_modified = load_from_json("data.json")
        linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)  

        all_linelevel_splits = []      
        for line in linelevel_subtitles:
            out = create_caption(line, video_size)
            all_linelevel_splits.extend(out)

        final_video = CompositeVideoClip([blank_clip] + all_linelevel_splits)
        final_video = final_video.set_audio(audio)
        return final_video

    else:
        
        with PILImage.open(image_path) as img:
            img = resize_image_to_fit_video(img, video_size)
            img.save("temp_resized_image.png")
        
        img_clip = ImageClip("temp_resized_image.png", duration=audio_duration).set_audio(audio)
    
        return img_clip


def process_video_with_multiple_sounds(video_path, image_audio_pairs, silent_audio_path, POST_TYPE):
    base_video = VideoFileClip(video_path)
    video_fps = base_video.fps  # Get fps from the original video
    
    silent_clip = AudioFileClip(silent_audio_path)
    clips = []

    composite_clip=None
    if POST_TYPE == "askReddit":
        for image_path, audio_path in image_audio_pairs:
            img_clip = image_and_sound_to_video(image_path, audio_path, base_video.size)
            clips.append(img_clip)
            clips.append(ColorClip(base_video.size, color=(0,0,0), duration=silent_clip.duration))  # black frame during silence

        image_audio_sequence = concatenate_videoclips(clips[:-1])  # Excluding the last silent clip
        image_audio_sequence.fps = video_fps  # Set fps for the concatenated clip

        # Overlay the image-audio sequence onto the base video
        composite_clip = CompositeVideoClip([base_video, image_audio_sequence.set_position("center").crossfadein(0.5)])
    elif POST_TYPE == "storyPost":
        if (len(image_audio_pairs) != 2):
            raise("storyPost must have exactly 2 image_audio_pair")

        for index, (image_path, audio_path) in enumerate(image_audio_pairs):
            if index == 0:  # For the first iteration
                audio_clip = image_and_sound_to_video(image_path, audio_path, base_video.size, True)
            else:
                audio_clip = image_and_sound_to_video(image_path, audio_path, base_video.size, False, POST_TYPE)
            
            clips.append(audio_clip)
            clips.append(ColorClip(base_video.size, color=(0,0,0), duration=silent_clip.duration))

        image_audio_sequence = concatenate_videoclips(clips[:-1])  # Excluding the last silent clip
        image_audio_sequence.fps = video_fps  # Set fps for the concatenated clip

        # Overlay the image-audio sequence onto the base video
        composite_clip = CompositeVideoClip([base_video, image_audio_sequence.set_position("center").crossfadein(0.2)])

    composite_clip.write_videofile("output.mp4")
    return './output.mp4'


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

    # Example image and audio pairs
    image_audio_pairs = [
        ("./util/input/reddit_posts/16bn0gy_t1_jze3jfj.png", "./util/input/reddit_posts/test1.mp3"),
        ("./util/input/reddit_posts/16bn0gy_t1_jze38dn.png", "./util/input/reddit_posts/test2.mp3"),
        # Add more pairs as needed
    ]

    silent_audio_path = "./util/input/silent.mp3"
    process_video_with_multiple_sounds(video_path, image_audio_pairs, silent_audio_path)

    upload_video("output.mp4")

    # Cleanup
    os.remove("temp_resized_image.png")
