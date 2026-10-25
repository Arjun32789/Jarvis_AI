from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os

# Tumhara Chrome profile use karo taaki login yaad rahe
CHROME_PROFILE = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--user-data-dir={CHROME_PROFILE}")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def instagram_action(action, query="", text=""):
    driver = get_driver()
    try:
        if action == "open":
            driver.get("https://www.instagram.com")
            time.sleep(5)

        elif action == "profile":
            driver.get(f"https://www.instagram.com/{query}/")
            time.sleep(5)

        elif action == "search":
            driver.get("https://www.instagram.com/explore/search/")
            time.sleep(4)
            try:
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))
                )
                search_box.send_keys(query)
                time.sleep(3)
            except:
                print("Search box not found - login required")

        elif action == "like":
            try:
                like_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[name()="svg"][@aria-label="Like"]'))
                )
                like_btn.click()
                print("Liked!")
            except Exception as e:
                print(f"Like failed: {e}")

        elif action == "story":
            driver.get("https://www.instagram.com/stories/")
            time.sleep(4)

        elif action == "reels":
            driver.get("https://www.instagram.com/reels/")
            time.sleep(4)

        elif action == "explore":
            driver.get("https://www.instagram.com/explore/")
            time.sleep(4)

        elif action == "messages":
            driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(4)

        print("Closing in 10 sec...")
        time.sleep(10)
    except Exception as e:
        print(f"Instagram error: {e}")
        time.sleep(3)
    finally:
        try:
            driver.quit()
        except:
            pass

def twitter_action(action, query="", text=""):
    driver = get_driver()
    try:
        if action == "open":
            driver.get("https://twitter.com")
            time.sleep(5)

        elif action == "post":
            driver.get("https://twitter.com/compose/tweet")
            time.sleep(5)
            try:
                tweet_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
                )
                tweet_box.click()
                time.sleep(1)
                tweet_box.send_keys(text)
                time.sleep(2)
                # Ctrl + Enter to post
                tweet_box.send_keys(Keys.CONTROL + Keys.ENTER)
                print(f"Tweeted: {text}")
            except Exception as e:
                print(f"Tweet failed: {e}")

        elif action == "search":
            driver.get(f"https://twitter.com/search?q={query}")
            time.sleep(5)

        elif action == "profile":
            driver.get(f"https://twitter.com/{query}")
            time.sleep(5)

        elif action == "trending":
            driver.get("https://twitter.com/explore/tabs/trending")
            time.sleep(5)

        elif action == "notifications":
            driver.get("https://twitter.com/notifications")
            time.sleep(4)

        elif action == "messages":
            driver.get("https://twitter.com/messages")
            time.sleep(4)

        print("Closing in 10 sec...")
        time.sleep(10)
    except Exception as e:
        print(f"Twitter error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

def facebook_action(action, query="", text=""):
    driver = get_driver()
    try:
        if action == "open":
            driver.get("https://www.facebook.com")
            time.sleep(5)

        elif action == "post":
            driver.get("https://www.facebook.com")
            time.sleep(5)
            try:
                post_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "What")]'))
                )
                post_box.click()
                time.sleep(2)
                # Popup mein type
                text_area = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
                )
                text_area.send_keys(text)
                time.sleep(2)
                print(f"Post drafted: {text}")
            except Exception as e:
                print(f"Post failed: {e}")

        elif action == "profile":
            driver.get(f"https://www.facebook.com/{query}")
            time.sleep(5)

        elif action == "messages":
            driver.get("https://www.facebook.com/messages")
            time.sleep(4)

        elif action == "notifications":
            driver.get("https://www.facebook.com/notifications")
            time.sleep(4)

        elif action == "friends":
            driver.get("https://www.facebook.com/friends")
            time.sleep(4)

        print("Closing in 10 sec...")
        time.sleep(10)
    except Exception as e:
        print(f"Facebook error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

def linkedin_action(action, query=""):
    driver = get_driver()
    try:
        if action == "open":
            driver.get("https://www.linkedin.com")
            time.sleep(5)
        elif action == "profile":
            driver.get(f"https://www.linkedin.com/in/{query}")
            time.sleep(5)
        elif action == "messages":
            driver.get("https://www.linkedin.com/messaging/")
            time.sleep(4)
        elif action == "notifications":
            driver.get("https://www.linkedin.com/notifications/")
            time.sleep(4)
        elif action == "jobs":
            driver.get("https://www.linkedin.com/jobs/")
            time.sleep(4)
        elif action == "feed":
            driver.get("https://www.linkedin.com/feed/")
            time.sleep(4)
        print("Closing in 10 sec...")
        time.sleep(10)
    except Exception as e:
        print(f"LinkedIn error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

def reddit_action(action, query=""):
    driver = get_driver()
    try:
        if action == "open":
            driver.get("https://www.reddit.com")
            time.sleep(5)
        elif action == "search":
            driver.get(f"https://www.reddit.com/search/?q={query}")
            time.sleep(5)
        elif action == "popular":
            driver.get("https://www.reddit.com/r/popular/")
            time.sleep(4)
        print("Closing in 10 sec...")
        time.sleep(10)
    except Exception as e:
        print(f"Reddit error: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    platform = sys.argv[1] if len(sys.argv) > 1 else ""
    action = sys.argv[2] if len(sys.argv) > 2 else ""
    query = sys.argv[3] if len(sys.argv) > 3 else ""
    text = sys.argv[4] if len(sys.argv) > 4 else ""
    
    if platform == "instagram":
        instagram_action(action, query, text)
    elif platform == "twitter":
        twitter_action(action, query, text)
    elif platform == "facebook":
        facebook_action(action, query, text)
    elif platform == "linkedin":
        linkedin_action(action, query)
    elif platform == "reddit":
        reddit_action(action, query)
    else:
        print("Usage: python social_auto.py <platform> <action> [query] [text]")
        print("Platforms: instagram, twitter, facebook, linkedin, reddit")