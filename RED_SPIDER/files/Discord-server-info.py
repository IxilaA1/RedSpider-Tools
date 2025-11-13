import requests
import json
import sys

def get_server_info(bot_token, server_id):
    """
    Retrieves detailed information about a Discord Guild (Server).

    :param bot_token: The Discord Bot token (must be a member of the server).
    :param server_id: The ID of the target server.
    :return: The dictionary containing the server data, or None on failure.
    """
    if not all([bot_token, server_id]):
        print("Error: Bot Token and Server ID must both be provided.")
        return None

    # Discord API Endpoint for getting Guild information
    API_ENDPOINT = f"https://discord.com/api/v10/guilds/{server_id}"

    # HTTP Headers must contain the Bot Token for authorization
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    try:
        # Send the GET request to the API
        response = requests.get(API_ENDPOINT, headers=headers)
        
        # Check for success (Discord returns 200 OK)
        if response.status_code == 200:
            server_data = response.json()
            return server_data
        
        # Handle errors
        else:
            print(f"ERROR: API request failed with status code {response.status_code}.")
            print("Response content:")
            try:
                # Attempt to display the Discord error message
                print(json.dumps(response.json(), indent=4))
            except json.JSONDecodeError:
                print(response.text)
            
            return None

    except requests.exceptions.RequestException as e:
        print(f"\nConnection or HTTP Error occurred: {e}")
        print("Please check your network connection or the provided inputs.")
        return None

# --- Main script execution ---

print("--- DISCORD SERVER INFO RETRIEVER TOOL ---")

try:
    # 1. Ask the user for required inputs
    BOT_TOKEN = input("Enter your Discord Bot Token (REQUIRED: Bot must be in the target server): ").strip()
    
    SERVER_ID = input("Enter the TARGET SERVER ID (Guild ID): ").strip()
    
    if not SERVER_ID.isdigit() or len(SERVER_ID) < 17:
        print("Error: Invalid Server ID format. Must be a numeric ID.")
        sys.exit(1)

    # 2. Execute the retrieval function
    print("\nAttempting to fetch server information...")
    info = get_server_info(BOT_TOKEN, SERVER_ID)

    # 3. Display the results
    if info:
        print("\n--- SERVER INFORMATION SUCCESS ---")
        print(f"Name: {info.get('name', 'N/A')}")
        print(f"ID: {info.get('id', 'N/A')}")
        print(f"Owner ID: {info.get('owner_id', 'N/A')}")
        print(f"Member Count: {info.get('approximate_member_count', info.get('member_count', 'N/A'))}")
        print(f"Verification Level: {info.get('verification_level', 'N/A')}")
        print(f"Boost Level (Tier): {info.get('premium_tier', 'N/A')}")
        print(f"Description: {info.get('description', 'N/A')}")
        print(f"Features: {', '.join(info.get('features', []))}")
        
        print("\n--- Raw Data Snippet ---")
        # Displaying a subset of the data for quick reference
        keys_to_show = ['name', 'id', 'owner_id', 'member_count', 'verification_level', 'premium_tier']
        snippet = {k: info[k] for k in keys_to_show if k in info}
        print(json.dumps(snippet, indent=4))
    else:
        print("\nFailed to retrieve server information. Check the Bot Token, Server ID, and if the bot is in the server.")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")