import os
from moviepy.editor import VideoFileClip, vfx

def to_snake_case(name):
    s1 = name.replace('-', ' ').replace('.', ' ').title().replace(' ', '')
    return ''.join(['_' + i.lower() if i.isupper() else i for i in s1]).lstrip('_')

def crop_to_vertical(input_path):
    # Load the video
    clip = VideoFileClip(input_path)
    
    # Get video dimensions
    width, height = clip.size
    
    # Calculate new width and height
    new_width = height * 9/16
    new_height = height
    
    # Calculate cropping margins (although they're not used in the cropping step)
    left_margin = (width - new_width) / 2
    right_margin = width - new_width - left_margin
    
    # Crop the video using vfx.crop
    cropped_clip = vfx.crop(clip, x_center=width/2, width=int(new_width), y_center=height/2, height=int(new_height))
    
    # Extract file name and extension
    file_name, file_extension = os.path.splitext(os.path.basename(input_path))
    
    # Convert filename to snake_case
    snake_case_name = to_snake_case(file_name)
    
    # Create the output path
    output_path = os.path.join(os.path.dirname(input_path), snake_case_name + file_extension)
    
    # Write the video to the output path with a higher bitrate
    cropped_clip.write_videofile(output_path, codec="libx264", bitrate="5000k", audio_bitrate="320k", ffmpeg_params=["-crf", "18"])

    return output_path
