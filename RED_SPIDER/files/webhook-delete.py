import requests

def delete_webhook(webhook_url):
    """
    Sends a DELETE request to the Discord Webhook URL to permanently delete it.

    :param webhook_url: The complete Discord Webhook URL.
    :return: True if deletion was successful, False otherwise.
    """
    if not webhook_url:
        print("Error: Webhook URL is empty.")
        return False

    try:
        # A DELETE request to the webhook URL will remove it.
        # This request requires no body.
        print(f"Attempting to delete webhook: {webhook_url}")
        response = requests.delete(webhook_url)

        # Discord returns a 204 No Content status code upon successful deletion.
        if response.status_code == 204:
            print("\nSUCCESS: Webhook has been permanently deleted.")
            return True
        
        # Handle common Discord API errors
        elif response.status_code == 404:
            print("\nERROR: 404 Not Found. The webhook may have already been deleted or the URL is invalid.")
        elif response.status_code == 401:
            print("\nERROR: 401 Unauthorized. The webhook URL is likely invalid or incomplete.")
        else:
            # Handle other HTTP errors
            response.raise_for_status() 
            
        return False

    except requests.exceptions.RequestException as e:
        print(f"\nConnection or HTTP Error occurred: {e}")
        print("Please check your network connection or the provided URL.")
        return False

# --- Main script execution ---

print("--- DISCORD WEBHOOK DELETION TOOL ---")

# Prompt the user for the webhook URL
WEBHOOK_LINK = input("Enter the full Discord Webhook URL you want to DELETE: ")

# WARNING: Confirm the action as it's irreversible
print("\n--- WARNING: THIS ACTION IS PERMANENT ---")
confirmation = input("Type 'DELETE' to confirm irreversible deletion of this webhook: ")

if confirmation.upper() == "DELETE":
    # Execute the deletion function
    success = delete_webhook(WEBHOOK_LINK)
    if not success:
        print("Deletion failed.")
else:
    print("\nDeletion cancelled by user.")