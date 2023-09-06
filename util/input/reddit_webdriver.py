import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import praw
from time import sleep
from pyvirtualdisplay import Display

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

    # Ensure the URL is a valid Reddit URL
    if 'www.reddit.com' not in components:
        return None, None, None
    
    # Ensure the URL contains 'r' and 'comments' indicating it's a post or comment URL
    if 'r' not in components or 'comments' not in components:
        return None, None, None
    
    # Extract subreddit name
    try:
        r_index = components.index('r')
        subreddit_name = components[r_index + 1]
    except (ValueError, IndexError):
        subreddit_name = None
    
    # Extract post ID
    try:
        post_index = components.index('comments')
        post_id = components[post_index + 1]
    except (ValueError, IndexError):
        post_id = None

    # Extract the comment ID if exists
    try:
        comment_index = components.index('comment')
        comment_id = components[comment_index + 1]
    except (ValueError, IndexError):
        comment_id = None

    return subreddit_name, post_id, comment_id

def get_comments(subreddit_name, post_id, comment_id=None):
    post = r.submission(id=post_id)
    post.comments.replace_more(limit=None)
    comments = post.comments.list()

    comment_details = []  # List to store details about each comment

    for comment in comments:
        cmts = "https://www.reddit.com" + post.permalink
        drv.get(cmts)

        id = f"t1_{comment.id}"
        try:
            cmt = WebDriverWait(drv, timeout).until(lambda x: x.find_element(By.ID, id))
            scroll_to_element(cmt)
        except TimeoutException:
            print("Page load timed out...")
        else:
            screenshot_path = "./reddit_posts/" + post_id + "_" + id + ".png"
            cmt.screenshot(screenshot_path)
            comment_details.append({"text": comment.body, "screenshot_path": screenshot_path})

    return comment_details  # Return the list

def process_reddit_url(url_list):
    login()

    all_comment_details = []  # List to store details for all comments from all URLs

    for url in url_list:
        subreddit_name, post_id, comment_id = parse_reddit_url(url)
        if post_id:
            comment_details = get_comments(subreddit_name, post_id, comment_id)
            all_comment_details.append(comment_details)  # Add details for comments of current URL
        else:
            print("Invalid Reddit URL")
    
    return all_comment_details  # Return the combined list

