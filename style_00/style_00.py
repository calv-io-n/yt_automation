from moviepy.editor import *
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.all import *
from moviepy.video.tools.subtitles import SubtitlesClip

import json

config = {}
with open('example.json', 'r') as file:
    config = json.load(file)

all_clips = [VideoFileClip(config[0]['files'][0])]
max_width = max([clip.w for clip in all_clips])
max_height = max([clip.h for clip in all_clips])


TOTAL_CLIPS = []

# Scene 0
scene_0c0 = VideoFileClip(config[0]['files'][0], audio=False) # .crop(486, 180, 1196, 570)

w,h = moviesize = scene_0c0.size


scene_0c1 = (VideoFileClip(config[0]['files'][1], audio=False).
         resize((w/3,h/3)).    # one third of the total screen
         margin( 6,color=(255,255,255)).  #white margin
         margin( bottom=20, right=20, opacity=0). # transparent
         set_pos(('right','bottom')) )

scene_0 = CompositeVideoClip([scene_0c0,scene_0c1])
TOTAL_CLIPS.append(scene_0)


# Scene 1: Title
# Image file
image = config[1]['image']
text = config[1]['text']

color_clip = ColorClip((max_width, max_height), color=(0,0,0), duration=5)

# # Create ImageClip
scene_1img0 = ImageClip(image, duration=10).set_pos('center')

# # Create text clip
scene_1txt0 = (TextClip(text['content'], fontsize=70, color='white', font=text['font']).set_position('center').set_duration(10))

# # Overlay text on image
scene_1 = CompositeVideoClip([color_clip, scene_1img0, scene_1txt0])

TOTAL_CLIPS.append(scene_1)


# # FINAL ASSEMBLY
final_video = concatenate_videoclips(TOTAL_CLIPS)
final_video.write_videofile("final_output.mp4",
                          verbose=True,
                          codec="libx264",
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True, 
                          preset="medium",
                          ffmpeg_params=["-profile:v","baseline", "-level","3.0","-pix_fmt", "yuv420p"])