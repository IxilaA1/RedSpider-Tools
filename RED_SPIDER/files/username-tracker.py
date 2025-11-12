import requests
from requests.exceptions import RequestException

# Prioritized list of over 80 websites, focusing on common OSINT targets first.
SITES_TO_CHECK = {
    # 1. PRIMARY SOCIAL & MEDIA (High OSINT Value)
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "Twitter (X)": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Medium": "https://medium.com/@{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Imgur": "https://imgur.com/user/{}",
    "Tumblr": "https://{}.tumblr.com",
    
    # 2. DEVELOPMENT & PROFESSIONAL (Medium/High OSINT Value)
    "GitHub": "https://github.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}", # Reliability low via simple check
    "GitLab": "https://gitlab.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Behance": "https://www.behance.net/{}",
    "About.me": "https://about.me/{}",

    # 3. GAMING & ENTERTAINMENT
    "Steam": "https://steamcommunity.com/id/{}",
    "Roblox": "https://www.roblox.com/user/profile?username={}",
    "Last.fm": "https://www.last.fm/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    "Dailymotion": "https://www.dailymotion.com/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Newgrounds": "https://{}.newgrounds.com",
    
    # 4. COMMERCE, FORUMS & OTHER
    "Ebay": "https://www.ebay.com/usr/{}",
    "Etsy": "https://www.etsy.com/shop/{}",
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Trello": "https://trello.com/{}",
    "Gist": "https://gist.github.com/{}",
    "500px": "https://500px.com/p/{}",
    "AngelList": "https://angel.co/{}",
    "Ask.fm": "https://ask.fm/{}",
    "BuzzFeed": "https://www.buzzfeed.com/{}",
    "Coderwall": "https://coderwall.com/{}",
    "Discogs": "https://www.discogs.com/user/{}",
    "Disqus": "https://disqus.com/by/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "Drupal": "https://www.drupal.org/u/{}",
    "Duolingo": "https://www.duolingo.com/profile/{}",
    "Flipboard": "https://flipboard.com/@{}",
    "Foursquare": "https://foursquare.com/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Gravatar": "https://gravatar.com/{}",
    "HubPages": "https://{}.hubpages.com",
    "Ifunny": "https://ifunny.co/user/{}",
    "Instapaper": "https://www.instapaper.com/p/{}",
    "Issuu": "https://issuu.com/{}",
    "Keybase": "https://keybase.io/{}",
    "LiveJournal": "https://{}.livejournal.com",
    "Meetup": "https://www.meetup.com/members/{}",
    "Patreon": "https://www.patreon.com/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "ReadTheDocs": "https://readthedocs.org/profiles/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",
    "Scratch": "https://scratch.mit.edu/users/{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "Telegram": "https://t.me/{}",
    "TripAdvisor": "https://www.tripadvisor.com/members/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "VSCO": "https://vsco.co/{}",
    "Weibo": "https://weibo.com/{}",
    "Academia.edu": "https://academia.edu/{}",
    "Carbonmade": "https://{}.carbonmade.com",
    "Coroflot": "https://www.coroflot.com/{}",
    "CreativeMarket": "https://creativemarket.com/{}",
    "LastPass": "https://lastpass.com/user/{}",
    "ProtonMail": "https://protonmail.com/@{}",
}

def check_username_availability(username):
    """
    Checks if the username exists on the specified websites one by one and prints the result immediately.
    """
    print(f"\nStarting OSINT check for username: {username}\n")
    print("-" * 50)
    print(f"{'Website':<20} | Result")
    print("-" * 50)
    
    # results = {} # Removed storage, printing directly

    for site, base_url in SITES_TO_CHECK.items():
        profile_url = base_url.format(username)
        
        try:
            response = requests.get(profile_url, stream=True, timeout=10)
            
            # 200 (OK) means profile exists (TAKEN).
            # 404 (Not Found) or 403 (Forbidden) means AVAILABLE.
            if response.status_code == 200:
                result = f"TAKEN (URL: {profile_url})"
            elif response.status_code == 404 or response.status_code == 403:
                result = "AVAILABLE"
            else:
                result = f"UNKNOWN"
                
        except RequestException as e:
            result = f"ERROR (Connection failed: {e})"
        finally:
            if 'response' in locals():
                response.close()
            
            # Print result immediately after checking the site
            print(f"{site:<20} | {result}")

    print("-" * 50)
    print("Check complete.")


def main():
    """
    Main function to prompt for username and run the check.
    """
    try:
        username = input("Enter the username to check: ").strip()
        
        if not username:
            print("Username cannot be empty.")
            return

        # Run the check
        check_username_availability(username)

    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")

if __name__ == "__main__":
    main()