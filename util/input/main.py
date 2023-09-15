import os
import random
from flask import Flask, render_template, request, jsonify
from reddit_webdriver import process_reddit_urls, parse_reddit_url
from speech import generate_speech
from compile_movie import process_video_with_multiple_sounds
from uploader import upload_to_drive

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create_video', methods=['POST'])
def create_video():
    # Checking if the request contains JSON data and the key 'post_url'

    if not request.json or 'post_url' not in request.json:
        return jsonify({"status": "error", "message": "Missing JSON data."})

    # Checking if the request contains JSON data and the key 'comment_url_list'
    POST_TYPE = request.json['POST_TYPE']

    post_id = parse_reddit_url(request.json['post_url']).get('post_id')
    # Assuming post_id has been parsed using parse_reddit_url
    post_folder_path = os.path.join('./util/input/reddit_posts', post_id)

    # Check if the folder exists, if not, create it
    if not os.path.exists(post_folder_path):
        os.makedirs(post_folder_path)

    # 1. Selenium Webdriver Retrieval
    print("Processing Reddit URLs...")
    post_url = request.json['post_url']
    comment_url_list = request.json['comment_url_list']
    text_screenshot_list = process_reddit_urls(post_url, comment_url_list, POST_TYPE)

    print(text_screenshot_list)

    if not text_screenshot_list:
        return jsonify({"status": "error", "message": "Error processing Reddit URLs."})

    # 2. Text-to-Speech
    print("Processing text to speech...")
    image_audio_pairs = []

    # Do Title to maybe separate hook further out
    title_speech_result = generate_speech(text_screenshot_list[0].get('title'), post_folder_path)
    image_audio_pairs.append(text_screenshot_list[0].get('screenshot_path'),title_speech_result.get('audio_path'))

    # Process the rest of the text
    for reddit_element in text_screenshot_list:
        rest_speech_result = generate_speech(reddit_element.get('text'), post_folder_path)
        image_audio_pairs.append(reddit_element.get('screenshot_path'),rest_speech_result.get('audio_path'))


    # 3. Video Compilation
    print("Processing video...")
    subfolder_path = "./util/input/starters"

    mp4_files = [f for f in os.listdir(subfolder_path) if f.endswith('.mp4')]
    if not mp4_files:
        print("No MP4 files found in the subfolder!")
        exit()

    random_video = random.choice(mp4_files)
    video_path = os.path.join(subfolder_path, random_video)
    silent_audio_path = "./util/input/silent.mp3"
    finished_path = process_video_with_multiple_sounds(video_path, image_audio_pairs, silent_audio_path, POST_TYPE)

    # 4. Upload to Google Drive
    upload_to_drive(finished_path)

    # Mock results for demonstration
    success = True
    google_drive_link = "https://drive.google.com/path_to_video"

    if success:
        return jsonify({"status": "success", "link": google_drive_link})
    else:
        return jsonify({"status": "error", "message": "Error creating video."})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
