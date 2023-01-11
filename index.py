from moviepy.editor import VideoFileClip, CompositeVideoClip, VideoClip, vfx

# Open the video file
clip = VideoFileClip("input.mp4")

# Create a fade-in effect by gradually increasing the opacity of the clip from 0 to 1 over the first second
def fadein(t):
    if t < 1.0:
        return t
    else:
        return 1.0
faded_clip = clip.fx(vfx.fadein, 1.0)

# Save the output
faded_clip.write_videofile("output.mp4")
