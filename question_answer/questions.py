import numpy as np
from moviepy.editor import *
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.all import *
# from moviepy.video.tools.subtitles import SubtitlesClip

sys.path.append('../') # this will add the parent directory to the path
from image_fx import pulse, fadeout
from image_edit import clip_img_format

import json

config = {}
with open('example.json', 'r') as file:
    config = json.load(file)

# List all Images from config
all_clips = [VideoFileClip(config["question_template"]), VideoFileClip(config["intro"]),]
max_width = max([clip.w for clip in all_clips])
max_height = max([clip.h for clip in all_clips])


TOTAL_GENERATED_CLIPS = []

# Title
scene_0c0 = VideoFileClip(config["intro"], audio=False) # .crop(486, 180, 1196, 570)
TOTAL_GENERATED_CLIPS.append(scene_0c0)


# Questions
question_base_clip = VideoFileClip(config["question_template"], audio=False)
for question in config['questions']:
    question_text = question["question_text"]
    answer_image = question['answer_image']
    answer_text = question['answer_text']

    # color_clip = ColorClip((max_width, max_height), color=(0,0,0), duration=5)

    # # Create ImageClip
    question_text_clip = (TextClip(question_text, fontsize=30, color='white', font="Arial").set_position('left').set_duration(5))
    answer_text_clip = (TextClip(answer_text, fontsize=30, color='white', font="Arial").set_position('left').set_duration(5))
    answer_image_clip = ImageClip(np.array(clip_img_format(answer_image))).set_duration(4)

    # apply the effect to the ImageClip
    answer_image_clip = answer_image_clip.fadeout(2, color=(255,255,255))
    answer_image_clip = answer_image_clip.resize(lambda t : pulse(t)).set_pos('center')
    answer_image_clip = answer_image_clip.set_pos('right')
  
    # # Overlay text on image
    scene = CompositeVideoClip([question_base_clip, question_text_clip, answer_text_clip, answer_image_clip])

    TOTAL_GENERATED_CLIPS.append(scene)

# FINAL ASSEMBLY
final_video = concatenate_videoclips(TOTAL_GENERATED_CLIPS)
final_video.write_videofile(f"../dist/{config['title']}.mp4")