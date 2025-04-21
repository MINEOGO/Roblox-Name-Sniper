import requests
import time
from colorama import Fore, Style, init

init()

WEBHOOK_URL = "you thought lol"

# Track elapsed time
start_time = time.time()

def send_discord_message(content, embed=None):
    data = {"content": content}
    if embed:
        data["embeds"] = [embed]
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(WEBHOOK_URL, json=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error sending to Discord: {e}" + Style.RESET_ALL)

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    try:
        response = requests.get(url)
        response_data = response.json()

        code = response_data.get("code")
        if code == 0:  # Valid username
            print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
            with open("valid.txt", "a") as valid_file:
                valid_file.write(username + "\n")
            
            # Send to Discord as an embed
            embed = {
                "title": "VALID USERNAME FOUND",
                "fields": [
                    {"name": "LETTERS", "value": "4", "inline": True},  # Assuming 4 is the fixed number of letters
                    {"name": "Username", "value": username, "inline": True},
                ],
                "color": 3066993  # Green color
            }
            send_discord_message("A valid username was found:", embed)
        
        elif code == 1:  # Taken username
            print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
        
        elif code == 2:  # Censored username
            print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
        
        else:
            print(Fore.YELLOW + f"bruh ({code}): {username}" + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"glitch {username}: {e}" + Style.RESET_ALL)

def main():
    # Send "script has started" message to Discord
    send_discord_message("Script has started.")

    with open("usernames.txt", "r") as file:
        usernames = file.read().splitlines()

    for username in usernames:
        # Check if 2 minutes have passed and pause if needed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 120:  # 2 minutes
            print(Fore.YELLOW + "Pausing for 2 minutes to avoid rate-limiting..." + Style.RESET_ALL)
            time.sleep(120)  # Pause for 2 minutes
            start_time = time.time()  # Reset the timer

        check_username(username)
        time.sleep(0.05)  # Delay between requests to avoid rate limiting

if __name__ == "__main__":
    main()
