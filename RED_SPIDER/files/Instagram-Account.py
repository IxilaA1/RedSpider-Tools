import instaloader
import sys
import os
import contextlib
import datetime

# --- Basic function and variable definitions to simulate an environment ---
# NOTE: These replace the undefined functions/variables in the original script.
# If you are using a specific framework, replace these with your own definitions.

def print_error(e):
    """Simulates the ErrorModule/Error function."""
    print(f"[ERROR] : {e}")

def get_current_time_str():
    """Returns the current formatted time."""
    return datetime.datetime.now().strftime("%H:%M:%S")

# Style variables (simulated)
BEFORE = "["
AFTER = "]"
ERROR = "🛑"
INFO_ADD = "➕"
white = ""  # For display without color in standard terminal
reset = ""  # For display without color in standard terminal

print(f"--- Instagram Account Scraper ---")
# ------------------------------------------------------------------------------------

try:
    @contextlib.contextmanager
    def suppress_output():
        """A context manager to suppress stdout and stderr output."""
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = devnull
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

    def search_profile(username):
        """Searches for and returns the Instaloader loader and profile objects."""
        with suppress_output():
            loader = instaloader.Instaloader()
            # Optional login if necessary for private profiles or to avoid limits
            # loader.load_session_from_file("your_username", "your_username.session")
            profile = instaloader.Profile.from_username(loader.context, username)
        return loader, profile

    # Request the username
    username = input(f"{BEFORE}{get_current_time_str()}{AFTER} [INPUT] Instagram Username -> {reset}")

    loader = None
    profile = None
    try:
        loader, profile = search_profile(username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"{BEFORE}{get_current_time_str()}{AFTER} {ERROR} Username '{username}' does not exist.")
        sys.exit(1) # Exit if profile does not exist
    except Exception as e:
        # This can catch rate limit errors (Too many requests)
        print(f"{BEFORE}{get_current_time_str()}{AFTER} {ERROR} Search error (limit exceeded or other) : {e}. Try again later.")
        sys.exit(1)

    # Displaying profile information
    print(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Full Name       : {white}{profile.full_name}
 {INFO_ADD} Username        : {white}{profile.username}
 {INFO_ADD} Instagram Id    : {white}{profile.userid}
 {INFO_ADD} Biography       : {white}{profile.biography}
 {INFO_ADD} Profile URL     : {white}https://instagram.com/{profile.username}
 {INFO_ADD} Profile Photo   : {white}{profile.profile_pic_url}
 {INFO_ADD} Posts           : {white}{profile.mediacount}
 {INFO_ADD} Followers       : {white}{profile.followers}
 {INFO_ADD} Following       : {white}{profile.followees}
 {INFO_ADD} Verified        : {white}{'True' if profile.is_verified else 'False'}
 {INFO_ADD} Private Account : {white}{'True' if profile.is_private else 'False'}
 {INFO_ADD} Business Account: {white}{'True' if profile.is_business_account else 'False'}""")

    if profile.is_business_account:
        print(f" {INFO_ADD} Business Category : {white}{profile.business_category_name}")

    print(f"{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")

    # Displaying the 5 latest posts
    # The original script checked if the account is NOT private OR if it's the logged-in user's account.
    # In this non-logged-in script, only the 'is_private' check is relevant.
    if not profile.is_private:
        print("\n--- 5 Latest Posts (Public Account) ---")
        try:
            posts = profile.get_posts()
            for i, post in enumerate(posts):
                # Simple cleanup of the caption
                caption_text = post.caption.replace('\n', ' ')[:100] + '...' if post.caption else 'None'
                print(f"""
 {INFO_ADD} Post n°{i+1}
 {INFO_ADD} URL         : {white}https://www.instagram.com/p/{post.shortcode}/
 {INFO_ADD} Date        : {white}{post.date}
 {INFO_ADD} Likes       : {white}{post.likes}
 {INFO_ADD} Comments    : {white}{post.comments}
 {INFO_ADD} Caption     : {white}{caption_text}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────""")
                if i == 4: # Limit to 5 posts (i=0 to i=4)
                    break
            print("\n--- End of posts ---")
        except Exception as e:
            print(f"\n{BEFORE}{get_current_time_str()}{AFTER} {ERROR} Error retrieving posts: {e}")
    else:
        print(f"{BEFORE}{get_current_time_str()}{AFTER} [INFO] Account is private. Cannot retrieve posts without logging in.")

except Exception as e:
    print_error(e)