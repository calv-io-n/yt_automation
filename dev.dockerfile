# Use selenium/standalone-chrome as the base image
FROM selenium/standalone-chrome

# Set the working directory in the container
WORKDIR /usr/src/app

# Install necessary utilities and libraries
USER root

# Install pip for Python3
RUN apt-get update && apt-get install -y python3-pip libasound2-dev xvfb ffmpeg

# Installing Python packages
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt selenium python-dotenv

# Install Xvfb for GUI display capabilities
RUN apt-get install -y xvfb

# Note: Since you're using `selenium/standalone-chrome`, Google Chrome and Chromedriver are already installed. 
# So, no need to reinstall them.

# Copy the rest of the application into the container
COPY . .

# Expose port 80
EXPOSE 80

# Flask environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=./util/input/main.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN chmod +x ./util/input/compile_movie.py

# Custom start script to run the application
CMD ["./util/input/compile_movie.py"]

# CMD ["./util/input/start.sh"]
