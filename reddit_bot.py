import praw
import config
import time

my_account = config.my_account
already_seen = []
terms = ["midterm", "cmput", "cs"]

def bot_login():
    try:
        print("Logging in...")
        r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = config.user_agent)
        print("Successfully logged in\n")
    except:
        print("Error logging in!\n")
        exit(1)
    return r

def run_bot(r):
    message = ""
    for post in r.subreddit(config.subreddit).new(limit = 20): #Limit the number of post we look at to 20
        for term in terms:
            if term in post.title.lower() or term in post.selftext.lower():
                # If the post has already been notified in a previous iteration, ignore
                if post.id in already_seen:
                    continue

                else:
                    message = message + f"Title: {post.title}\n\nText: {post.selftext}\n\n URL: {post.url}\n\n"
                    already_seen.append(post.id)

    if message == "":
        print("No new post with terms found")
        return
    try:
        r.redditor(my_account).message(subject = f"New post(s) containing terms", message = message)

    except praw.exceptions.APIException as e:
        if "USER_DOESNT_EXIST" in str(e):
            print("Recipient does not exist or does not allow direct messages.")
        else:
            print("Error:", e)
                    
    print("Bot completed iteration!")
    time.sleep(10) # Makse sure you don't send more than 30 request per minute

r = bot_login()
run_bot(r)

