import instaloader
from datetime import datetime
import time
from twilio.rest import Client
import threading
account_sid = ''  # Removed personal account SID
auth_token = ''  # Removed personal authentication token
twilio_phone_number = ''  # Removed personal Twilio phone number
recipient_phone_number = ['']  # Removed personal recipient phone number

sent_posts = set()

username = ''  # Removed personal username
password = ''  # Removed personal password


loader = instaloader.Instaloader()
loader.login(username, password)


def send_message(post_link,username):
    if post_link in sent_posts:
        print(f"Post already sent: {post_link}")
        return
    for i in recipient_phone_number:
        client = Client(account_sid, auth_token)
        message_body = f'NEW POST ALERT \n {username} just posted!\n Send over its summary as soon as possible,\n Good luck. \n {post_link}'
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=i
        )
        print(f'Message sent: {message.sid}')

    sent_posts.add(post_link)

def find_most_recent_date(date_list):
    if not date_list:
        return None

    most_recent_date = datetime.strptime(str(date_list[0]), "%Y-%m-%d %H:%M:%S")

    for date_string in date_list[1:]:
        date = datetime.strptime(str(date_string), "%Y-%m-%d %H:%M:%S")
        if date > most_recent_date:
            most_recent_date = date

    return most_recent_date

def fetch(loader,username):
    profile = instaloader.Profile.from_username(loader.context, username)
    recent_posts = profile.get_posts()
    post_dict = {}
    post_date_list = []
    latest_post = None
    count = 0
    for post in recent_posts:
        if count < 4:
            post_dict[post.date] = post
            post_date_list.append(post.date)
            count += 1
        else:
            break
    latest_post_date = find_most_recent_date(post_date_list)
    for post_data in post_dict:
        if post_data == latest_post_date:
            latest_post = post_dict[post_data]

    if latest_post:
        post_url = f"https://www.instagram.com/p/{latest_post.shortcode}/"
        print(post_url)
        send_message(post_url, username)

    else:
        print("No posts found.")

def fetch_recent_post(username):
    try:
        fetch(loader, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print("Invalid username. The profile does not exist.")
    except instaloader.exceptions.QueryReturnedBadRequestException as e:
        if "code 400" in str(e) or "429 - Too Many Requests" in str(e):
            try:
                loader1 = instaloader.Instaloader()
                fetch(loader1, username)
            except Exception as inner_e:
                print(f"Failed to fetch data. Error: {str(inner_e)}")
        else:
            print(f"Failed to fetch data. Error: {str(e)}")
    except Exception as e:
        print(f"Failed to fetch data. Error: {str(e)}")


def fetch_posts_periodically(username):
    while True:
        fetch_recent_post(username)
        time.sleep(180)  # Sleep for 3 minutes

if __name__ == "__main__":
    usernames = ["reign","dr_mudgil","antharris","yokkao","chasemcanear","designer_bag_exchange",'sevenzerooneseven'
                 ,"philip__villa","haitianbeauty25","trod","lorikassin"]  # Add more usernames if needed

    # Create and start a separate thread for each username
    threads = []
    for username in usernames:
        thread = threading.Thread(target=fetch_posts_periodically, args=(username,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

