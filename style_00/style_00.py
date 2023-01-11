from moviepy.editor import *
import json

config = {}
with open('example.json', 'r') as file:
    config = json.load(file)

scene_0c0 = VideoFileClip(config['files'][0], audio=False).\
               crop(486, 180, 1196, 570)

w,h = moviesize = scene_0c0.size


scene_0c1 = (VideoFileClip(config['files'][1], audio=False).
         resize((w/3,h/3)).    # one third of the total screen
         margin( 6,color=(255,255,255)).  #white margin
         margin( bottom=20, right=20, opacity=0). # transparent
         set_pos(('right','bottom')) )



# # A CLIP WITH A TEXT AND A BLACK SEMI-OPAQUE BACKGROUND

# txt = TextClip("V. Zulkoninov - Ukulele Sonata", font='Amiri-regular',
# 	               color='white',fontsize=24)

# txt_col = txt.on_color(size=(ukulele.w + txt.w,txt.h-10),
#                   color=(0,0,0), pos=(6,'center'), col_opacity=0.6)


# # THE TEXT CLIP IS ANIMATED.
# # I am *NOT* explaining the formula, understands who can/want.
# txt_mov = txt_col.set_pos( lambda t: (max(w/30,int(w-0.5*w*t)),
#                                   max(5*h/6,int(100*t))) )

# FINAL ASSEMBLY
scene_0 = CompositeVideoClip([scene_0c0,scene_0c1])
scene_0.subclip(0,5).write_videofile("./production.mp4",fps=24,codec='libx264')