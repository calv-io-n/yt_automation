# Use selenium/standalone-chrome as the base image
FROM selenium/standalone-chrome

# Set the working directory in the container
WORKDIR /usr/src/app

# Install necessary utilities and libraries
USER root

# Install pip for Python3, git and other dependencies
RUN apt-get update && apt-get install -y python3-pip libasound2-dev xvfb ffmpeg git
RUN apt-get update && apt-get install -y imagemagick

# Installing Python packages
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt selenium python-dotenv
RUN python3 -m pip install git+https://github.com/openai/whisper.git@248b6cb124225dd263bb9bd32d060b6517e067f8

# Install Xvfb for GUI display capabilities
RUN apt-get install -y xvfb

COPY ./util/input/policy.xml /etc/ImageMagick-6/policy.xml


# Note: Since you're using `selenium/standalone-chrome`, Google Chrome and Chromedriver are already installed. 
# So, no need to reinstall them.

# Copy the rest of the application into the container
COPY . .
COPY ./font.ttf /usr/share/fonts/

# Expose port 80
EXPOSE 80

# Flask environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=./util/input/main.py
ENV FLASK_RUN_HOST=0.0.0.0

# RUN chmod +x ./util/input/compile_movie.py
# RUN chmod +x ./util/input/reddit_webdriver.py

# Custom start script to run the application
# CMD ["./util/input/compile_movie.py"]
# CMD ["./util/input/reddit_webdriver.py"]
# CMD ["./util/input/reddit_webdriver.py"]
CMD ["./util/input/captions.py"]

# CMD ["./util/input/start.sh"]
