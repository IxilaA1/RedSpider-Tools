import random
import string
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to generate the unique code
def generate_code(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to send the generated URL to the webhook
def send_to_webhook(url, webhook_url):
    data = {
        "content": url
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Failed to send to webhook: {e}")

# Function to start the generating and sending process
def start_generating():
    # Ask for the webhook URL
    webhook_url = input("Please enter your Discord webhook URL: ")

    count = 1
    with ThreadPoolExecutor(max_workers=50) as executor:
        while True:
            code = generate_code()
            url = f"https://discord.gift/{code}"
            print(f"[{count}] Sent: {url}")
            
            # Submit the task to the executor to send the request asynchronously
            executor.submit(send_to_webhook, url, webhook_url)
            count += 1
            # Optionally, reduce sleep time if you want to send more requests per second
            # time.sleep(0.02)  # Sleep for 20 milliseconds (50 requests per second)

start_generating()