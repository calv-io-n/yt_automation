import os
from pytube import YouTube

def download_video(url, progressive=True, file_extension='mp4', highest_resolution=True):
    """
    Download a YouTube video.

    Parameters:
    - url (str): YouTube video URL.
    - progressive (bool): Filter by progressive streams. Defaults to True.
    - file_extension (str): File extension to filter by. Defaults to 'mp4'.
    - highest_resolution (bool): If True, download the highest resolution. If False, download the lowest resolution.

    Returns:
    - str: Path to the downloaded video.
    """
    yt = YouTube(url)
    
    # Filtering streams
    streams = yt.streams.filter(progressive=progressive, file_extension=file_extension)
    
    # Ordering streams by resolution
    if highest_resolution:
        streams = streams.order_by('resolution').desc()
    else:
        streams = streams.order_by('resolution').asc()
    
    selected_stream = streams.first()
    
    # Printing the resolution of the selected stream
    print(f"Resolution of the video being downloaded: {selected_stream.resolution}")
    
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(script_directory, "starters")  # Changed "backgrounds" to "starters"
    
    # Create the directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    return selected_stream.download(output_directory)

# Only runs the following code when the file is invoked directly
if __name__ == '__main__':
    url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
    downloaded_path = download_video(url)
    print(f"Video downloaded to: {downloaded_path}")
