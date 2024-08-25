import requests
import random
import string
import threading
webhook = "" # Your Webhook Here.
proxies = []
with open("proxies.txt", "r") as proxy_file:
    proxies = [line.strip() for line in proxy_file if line.strip()]

def tekostkos(usernames):
    username_list = "\n".join(usernames)
    embed = {
        "title": "Found Usernames!",
        "description": f"**Usernames:**\n{username_list}",
        "color": random.randint(10000000, 99999999)
    }
    payload = {"embeds": [embed]}
    return payload


def generate_username(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
found = set()
lock = threading.Lock()
def worker():
    while True:
        try:
            random_usernames = [generate_username() for _ in range(200)]
            api = "https://users.roproxy.com/v1/usernames/users"
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
            payload = {"usernames": random_usernames, "excludeBannedUsers": False}
            response = requests.post(api, headers=headers, json=payload, proxies={'http': random.choice(proxies)}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                found_usernames = [user_data['requestedUsername'] for user_data in data['data']]
                not_found_usernames = [username for username in random_usernames if username not in found_usernames]
                for username in not_found_usernames:
                    requests.post(webhook, json=tekostkos(not_found_usernames), proxies={'http': random.choice(proxies)}, timeout=5)
                    if username not in found: # Anti Duplicates
                        found.add(username)
                        print(f"NOT TAKEN | {username}")
        except requests.exceptions.ConnectionError as e:
            pass

num_threads = 10
threads = [threading.Thread(target=worker) for _ in range(num_threads)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
