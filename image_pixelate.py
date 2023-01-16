from moviepy.editor import *
import cv2

# Load the ImageClip
image = ImageClip("./assets_img/test.jpg")

# Get the width and height of the image
w, h = image.size

# Create the pixelation function
def pixelate_frame(t):
    # Scale the image down by the desired pixel size
    pixel_size = max(1, int(16*t))
    image_data = image.get_frame(t)
    pixelated_image = cv2.resize(image_data, (w//pixel_size, h//pixel_size), interpolation=cv2.INTER_NEAREST)

    # Scale the image back up to the original size
    pixelated_image = cv2.resize(pixelated_image, (w,h), interpolation=cv2.INTER_NEAREST)

    return pixelated_image

# Create the VideoClip
duration = 2 #duration of 2 seconds
pixelated_video = VideoClip(pixelate_frame, duration=duration)
pixelated_video = pixelated_video.fx(vfx.time_mirror)

# Save the pixelated video
pixelated_video.write_videofile("pixelated_video.mp4", fps=24)