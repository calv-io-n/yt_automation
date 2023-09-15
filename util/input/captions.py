#!/usr/bin/python3
import whisper
import json
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, VideoFileClip
import numpy as np


def transcribe_audio_with_whisper(audiofilename):
    model = whisper.load_model("medium")
    result = model.transcribe(audiofilename, word_timestamps=True)
    return result


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def split_text_into_lines(data):
    MaxChars = 80
    MaxDuration = 3.0
    MaxGap = 1.5

    subtitles = []
    line = []
    line_duration = 0
    line_chars = 0

    for idx, word_data in enumerate(data):
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)
        new_line_chars = len(temp)

        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx > 0:
            gap = word_data['start'] - data[idx-1]['end']
            maxgap_exceeded = gap > MaxGap
        else:
            maxgap_exceeded = False

        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0
                line_chars = 0

    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles


def create_caption(textJSON, framesize, font="Montserrat-ExtraBold", fontsize=80, color='white', bgcolor='purple'):
    wordcount = len(textJSON['textcontents'])
    full_duration = textJSON['end']-textJSON['start']

    word_clips = []
    xy_textclips_positions =[]
    
    x_pos = 0
    y_pos = 0
    # max_height = 0
    frame_width = framesize[0]
    frame_height = framesize[1]
    x_buffer = frame_width*1/10
    y_buffer = frame_height*1/5

    space_width = ""
    space_height = ""

    for index,wordJSON in enumerate(textJSON['textcontents']):
      duration = wordJSON['end']-wordJSON['start']
      word_clip = TextClip(wordJSON['word'], font = font,fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
      word_clip_space = TextClip(" ", font = font,fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
      word_width, word_height = word_clip.size
      space_width,space_height = word_clip_space.size
      if x_pos + word_width+ space_width > frame_width-2*x_buffer:
            # Move to the next line
            x_pos = 0
            y_pos = y_pos+ word_height+40

            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos+x_buffer,
                "y_pos": y_pos+y_buffer,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width +x_buffer, y_pos+y_buffer))
            x_pos = word_width + space_width
      else:
            # Store info of each word_clip created
            xy_textclips_positions.append({
                "x_pos":x_pos+x_buffer,
                "y_pos": y_pos+y_buffer,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width+ x_buffer, y_pos+y_buffer))

            x_pos = x_pos + word_width+ space_width


      word_clips.append(word_clip)
      word_clips.append(word_clip_space)  


    for highlight_word in xy_textclips_positions:
      
      word_clip_highlight = TextClip(highlight_word['word'], font = font,fontsize=fontsize, color=color,bg_color = bgcolor).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
      word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
      word_clips.append(word_clip_highlight)

    return word_clips


def create_audiogram(input_video_filename, linelevel_subtitles, output_filename):
    frame_size = (540, 960) # Important: This is the size of the video frame
    all_linelevel_splits = []

    for line in linelevel_subtitles:
        out = create_caption(line, frame_size)
        all_linelevel_splits.extend(out)

    input_video = VideoFileClip(input_video_filename)
    input_video_duration = input_video.duration
    background_clip = ColorClip(size=frame_size, color=(0, 0, 0)).set_duration(input_video_duration)

    final_video = CompositeVideoClip([background_clip] + all_linelevel_splits)
    final_video = final_video.set_audio(input_video.audio)

    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    # print(TextClip.list('font'))

    audiofilename = "util/input/reddit_posts/16bn0gy/f64b296f.wav"
    videofilename = "output.mp4"
    output_filename = "sub_output.mp4"

    transcription_result = transcribe_audio_with_whisper(audiofilename)

    wordlevel_info = []
    for segment in transcription_result['segments']:
        for word in segment['words']:
            wordlevel_info.append({'word': word['word'].strip(), 'start': word['start'], 'end': word['end']})

    save_to_json(wordlevel_info, "data.json")

    wordlevel_info_modified = load_from_json("data.json")

    # Fixing this line to call the function with wordlevel_info_modified as argument.
    linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)

    create_audiogram(videofilename, linelevel_subtitles, output_filename)