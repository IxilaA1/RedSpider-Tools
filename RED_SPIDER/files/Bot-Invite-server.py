import sys

def generate_bot_invite_link(bot_id, server_id, permissions=0, scope="bot"):
    """
    Generates the Discord OAuth2 invitation URL for a bot to join a specific server.

    :param bot_id: The application/client ID of the Discord bot.
    :param server_id: The ID of the guild (server) to invite the bot to.
    :param permissions: The integer value of the required permissions (0 for none/default).
    :param scope: The OAuth2 scope(s) required (e.g., 'bot', 'applications.commands').
    :return: The complete invitation URL string.
    """
    
    # Base URL for Discord OAuth2 authorization
    base_url = "https://discord.com/oauth2/authorize"
    
    # Constructing the query parameters
    params = {
        "client_id": bot_id,
        "scope": scope,
        "permissions": permissions,
        "guild_id": server_id,
        "disable_guild_select": "true" # Forces the selector to only show the target server
    }

    # Formatting parameters into a URL-friendly query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    
    # Final URL
    invite_url = f"{base_url}?{query_string}"
    
    return invite_url

# --- Main script execution ---

print("--- DISCORD BOT INVITE LINK GENERATOR ---")

try:
    # 1. Ask the user for required inputs
    BOT_ID = input("Enter the Discord Bot's CLIENT ID (Application ID): ").strip()
    
    # Basic validation for ID format (17-19 digits)
    if not BOT_ID.isdigit() or len(BOT_ID) < 17:
        print("Error: Invalid Bot ID format. Must be a numeric ID.")
        sys.exit(1)
        
    SERVER_ID = input("Enter the TARGET SERVER ID (Guild ID) for the bot: ").strip()
    
    if not SERVER_ID.isdigit() or len(SERVER_ID) < 17:
        print("Error: Invalid Server ID format. Must be a numeric ID.")
        sys.exit(1)

    # Note: We use 0 for permissions as a default. If specific permissions are needed, 
    # the user should provide the integer value (e.g., 8 for Administrator).
    PERMISSIONS_VALUE = input("Enter the REQUIRED PERMISSIONS integer value (Press Enter for default '0'): ").strip()
    
    # Default to 0 if the user enters nothing
    if not PERMISSIONS_VALUE:
        PERMISSIONS_VALUE = 0
    elif not PERMISSIONS_VALUE.isdigit():
        print("Error: Permissions value must be an integer.")
        sys.exit(1)
    else:
        PERMISSIONS_VALUE = int(PERMISSIONS_VALUE)

    # 2. Generate the link
    invite_link = generate_bot_invite_link(BOT_ID, SERVER_ID, PERMISSIONS_VALUE)

    # 3. Display the result
    print("\n--- INVITATION LINK GENERATED SUCCESSFULLY ---")
    print(f"Bot ID: {BOT_ID}")
    print(f"Target Server ID: {SERVER_ID}")
    print(f"Permissions Value: {PERMISSIONS_VALUE}")
    print("\n")
    print("COPY THIS URL AND PASTE IT IN YOUR BROWSER TO INVITE THE BOT:")
    print("----------------------------------------------------------")
    print(invite_link)
    print("----------------------------------------------------------")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")