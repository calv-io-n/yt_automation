from flask import Flask, render_template, request, jsonify
from reddit_webdriver import process_reddit_url
from speech import generate_speech

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create_video', methods=['POST'])
def create_video():
    # Checking if the request contains JSON data and the key 'reddit_url_list'
    if not request.json or 'reddit_url_list' not in request.json:
        return jsonify({"status": "error", "message": "Missing JSON data."})

    reddit_url_list = request.json['reddit_url_list']
    text_screenshot_list = process_reddit_url(reddit_url_list)

    if not text_screenshot_list:
        return jsonify({"status": "error", "message": "Error processing Reddit URLs."})


    speech_results = []
    for text in text_screenshot_list[0]:
        print(text)
        speech_result = generate_speech(text)
        speech_results.append(speech_result)

    # You can then process the speech_results list however you want.
    # For instance, you can combine them to create a video or upload them somewhere

    # Mock results for demonstration
    success = True
    google_drive_link = "https://drive.google.com/path_to_video"

    if success:
        return jsonify({"status": "success", "link": google_drive_link})
    else:
        return jsonify({"status": "error", "message": "Error creating video."})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
