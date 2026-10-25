from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def youtube_action(action, query="", text=""):
    driver = get_driver()
    try:
        if action == "play":
            print(f"Searching YouTube for: {query}")
            driver.get(f"https://www.youtube.com/results?search_query={query}")
            time.sleep(4)
            # Pehla video click karo
            first_video = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '(//ytd-video-renderer//a[@id="thumbnail"])[1]'))
            )
            first_video.click()
            print(f"Playing: {query}")
            time.sleep(5)

        elif action == "like":
            print("Looking for Like button...")
            like_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//like-button-view-model//button | //button[contains(@aria-label, "like this video")]'))
            )
            like_btn.click()
            print("Liked the video!")
            time.sleep(2)

        elif action == "subscribe":
            print("Looking for Subscribe button...")
            sub_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//yt-subscribe-button-view-model//button | //button[contains(@aria-label, "Subscribe")]'))
            )
            sub_btn.click()
            print("Subscribed!")
            time.sleep(2)

        elif action == "comment":
            print(f"Writing comment: {text}")
            driver.execute_script("window.scrollBy(0, 700)")
            time.sleep(2)
            comment_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//ytd-comment-simplebox-renderer//div[@id="contenteditable-root"] | //div[@id="simple-box"]//div[@contenteditable="true"]'))
            )
            comment_box.click()
            time.sleep(1)
            comment_box.send_keys(text)
            time.sleep(1)
            comment_box.send_keys(Keys.CONTROL + Keys.ENTER)
            print(f"Commented: {text}")
            time.sleep(2)

        elif action == "save":
            print("Looking for Save button...")
            save_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Save")] | //ytd-button-renderer[contains(@aria-label, "Save")]//button'))
            )
            save_btn.click()
            time.sleep(2)
            try:
                watch_later = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//yt-formatted-string[contains(text(), "Watch later")]'))
                )
                watch_later.click()
                print("Saved to Watch Later!")
            except:
                print("Save dialog appeared")
            time.sleep(2)

        elif action == "channel":
            print(f"Opening channel: {query}")
            driver.get(f"https://www.youtube.com/@{query}")
            time.sleep(5)

        else:
            print(f"Unknown action: {action}")

        # 10 second wait karo phir browser band
        print("Closing browser in 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    text = sys.argv[3] if len(sys.argv) > 3 else ""
    
    if not action:
        print("Usage: python youtube_auto.py <action> [query] [text]")
        print("Actions: play, like, subscribe, comment, save, channel")
        sys.exit(1)
    
    youtube_action(action, query, text)