from moviepy.editor import *

def create_video_from_image(image_path, audio_path, output_path, duration=10):
    # Load the image and set its duration
    clip = ImageClip(image_path).set_duration(duration)
    
    # Load the audio and trim it to the duration of the video
    audio = AudioFileClip(audio_path).subclip(0, duration)
    clip = clip.set_audio(audio)
    
    # Write the result to a file
    clip.write_videofile(output_path, fps=24)

if __name__ == "__main__":
    IMAGE_PATH = "path_to_your_image.jpg"
    AUDIO_PATH = "path_to_your_audio.mp3"
    OUTPUT_PATH = "output_video.mp4"
    
    create_video_from_image(IMAGE_PATH, AUDIO_PATH, OUTPUT_PATH)
