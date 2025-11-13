import requests
import json
import sys

def get_webhook_info(webhook_url):
    """
    Retrieves information about a Discord Webhook using its URL.

    :param webhook_url: The complete Discord Webhook URL (including the token).
    :return: A dictionary containing the webhook data or None on error.
    """
    if not webhook_url:
        print("Error: Webhook URL is empty.")
        return None

    try:
        # Perform a GET request to the webhook URL.
        # Discord returns a JSON object containing the webhook info.
        response = requests.get(webhook_url)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # The response body contains the webhook information in JSON
        webhook_data = response.json()

        return webhook_data

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: 404 Not Found. The webhook might be invalid or deleted.")
        elif response.status_code == 401:
            print(f"Error: 401 Unauthorized. The webhook URL is likely invalid.")
        else:
            print(f"HTTP Request Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
        print("Please check your internet connection or the provided URL.")
        return None
    except json.JSONDecodeError:
        print("JSON Decoding Error: The response is not valid JSON.")
        return None

# --- Main script execution ---

# 1. Ask the user for the webhook URL
print("--- DISCORD WEBHOOK INFO RETRIEVER ---")
WEBHOOK_LINK = input("Enter the full Discord Webhook URL: ")

# 2. Retrieve the information
info = get_webhook_info(WEBHOOK_LINK)

# 3. Display the results
if info:
    print("\n--- WEBHOOK INFORMATION SUCCESS ---")
    print(f"Webhook ID: {info.get('id', 'N/A')}")
    print(f"Name: {info.get('name', 'N/A')}")
    print(f"Channel ID: {info.get('channel_id', 'N/A')}")
    print(f"Guild (Server) ID: {info.get('guild_id', 'N/A')}")
    print(f"Type: {info.get('type', 'N/A')} (1: Incoming, 2: Channel Follower)")
    
    # Check if a User object is present (usually the bot/app that created it)
    user_info = info.get('user')
    if user_info:
        print("\n--- Creator/Owner User Info ---")
        print(f"User ID: {user_info.get('id', 'N/A')}")
        print(f"Username: {user_info.get('username', 'N/A')}")
        print(f"Discriminator: {user_info.get('discriminator', 'N/A')}")
        
    print("\n--- Raw Data Snippet ---")
    print(json.dumps({k: info[k] for k in ('id', 'name', 'channel_id', 'guild_id') if k in info}, indent=4))
else:
    print("\nFailed to retrieve webhook information.")