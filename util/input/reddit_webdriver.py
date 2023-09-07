#!/usr/bin/python3

import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from pyvirtualdisplay import Display
import praw

def set_mobile_resolution():
    drv.set_window_size(375, 812)

display = Display(visible=0, size=(800, 600))
display.start()

username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')

r = praw.Reddit(
    username=username,
    password=password,
    client_id=client_id,
    client_secret=client_secret,
    user_agent="voltage vibes",
)

opts = ChromeOptions()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

drv = Chrome(options=opts)
set_mobile_resolution()

timeout = 10

def login():
    if username is None:
        # Handle this case appropriately. For instance:
        raise ValueError("Username value is None!")

    drv.get('https://www.reddit.com/login/')

    # Wait for username field to appear
    user = WebDriverWait(drv, timeout).until(EC.presence_of_element_located((By.ID, "loginUsername")))
    user.send_keys(username)

    # Wait for password field to appear
    pwd = WebDriverWait(drv, timeout).until(EC.presence_of_element_located((By.ID, "loginPassword")))
    pwd.send_keys(password)

    # Wait for submit button to appear and click it
    btn = WebDriverWait(drv, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    btn.click()
    sleep(timeout)

    # Kill cookie agreement popup if it appears
    try:
        cookie = WebDriverWait(drv, timeout).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Accept all"]')))
        cookie.click()
    except TimeoutException:
        print("Cookie agreement popup didn't appear.")

    sleep(timeout)

def scroll_to_element(element):
    drv.execute_script("arguments[0].scrollIntoView(true);", element)
    sleep(2)  # Give it a moment to scroll

def parse_reddit_url(url):
    components = url.split("/")

    # Clean up the components by removing empty strings
    components = [c for c in components if c]

    # Ensure the URL is a valid Reddit URL
    if not any(domain in components for domain in ['www.reddit.com', 'reddit.com']):
        return {'subreddit': None, 'post_id': None, 'comment_id': None}

    # Extract details
    subreddit_name = components[components.index('r') + 1] if 'r' in components else None
    post_id = components[components.index('comments') + 1] if 'comments' in components else None
    comment_id = components[components.index('comments') + 3] if 'comments' in components and len(components) > components.index('comments') + 3 else None

    return {'subreddit': subreddit_name, 'post_id': post_id, 'comment_id': comment_id}

def hide_topbar():
    # Find all header tags on the page
    header = drv.find_element(By.TAG_NAME, 'header')

    print(header)

    # Iterate through each header and hide it
    drv.execute_script("arguments[0].remove();", header)

def get_comment(submission, post_id, comment_id):
    comment = submission.comments(comment_id)
    cmts = "https://www.reddit.com" + comment.permalink
    drv.get(cmts)
    hide_topbar()

    id = f"t1_{comment_id}"
    screenshot_path = None
    try:
        cmt = WebDriverWait(drv, timeout).until(lambda x: x.find_element(By.ID, id))
        scroll_to_element(cmt)
    except TimeoutException:
        print("Page load timed out...")
    else:
        screenshot_path = f"./util/input/reddit_posts/{post_id}/{post_id}_{id}.png"
        cmt.screenshot(screenshot_path)
        
    return {"text": comment.body, "screenshot_path": screenshot_path}

def get_post(submission, post_id):
    id = f"t3_{post_id}"
    cmts = "https://www.reddit.com" + submission.permalink
    hide_topbar()
    drv.get(cmts)

    screenshot_path = None
    try:
        cmt = WebDriverWait(drv, timeout).until(lambda x: x.find_element(By.ID, id))
        scroll_to_element(cmt)
    except TimeoutException:
        print("Page load timed out...")
    else:
        screenshot_path = f"./util/input/reddit_posts/{post_id}/{post_id}_{id}.png"
        cmt.screenshot(screenshot_path)
    
    return {"title": submission.title, "text": submission.selftext, "screenshot_path": screenshot_path}

def process_reddit_urls(root_url, comment_url_list):
    login()

    results = []

    parsed_url = parse_reddit_url(root_url)
    subreddit_name = parsed_url['subreddit']
    post_id = parsed_url['post_id']
    submission = r.submission(id=post_id)

    results.append(get_post(submission, post_id))

    for comment_url in comment_url_list:
        parsed_comment_url = parse_reddit_url(comment_url)
        subreddit_name = parsed_comment_url['subreddit']
        post_id = parsed_comment_url['post_id']
        comment_id = parsed_comment_url['comment_id']

        if post_id and comment_id:
            results.append(get_comment(submission, post_id, comment_id))
        else:
            print("Invalid Reddit URL")
    
    return results  # Return the combined list of results

if __name__ == "__main__":
    r.submission('16bn0gy')
    test = r.comment('jze38dn')
    print(test.body)
