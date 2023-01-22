from flask import Flask
import requests
import threading
import json

app = Flask(__name__)

@app.route("/")
def social_network_activity():
    tweets = []
    facebook_posts = []
    instagram_posts = []

    twitter_thread = threading.Thread(target=get_activity_count, args=(tweets, "https://takehome.io/twitter", ))
    facebook_thread = threading.Thread(target=get_activity_count, args=(facebook_posts, "https://takehome.io/facebook", ))
    instagram_thread = threading.Thread(target=get_activity_count, args=(instagram_posts,"https://takehome.io/instagram", ))

    twitter_thread.start()
    facebook_thread.start()
    instagram_thread.start()

    twitter_thread.join()
    facebook_thread.join()
    instagram_thread.join()

    activity = {"instagram": instagram_posts[0], "facebook": facebook_posts[0], "twitter":tweets[0]}

    json_response = json.dumps(activity, indent=4)
    return json_response

def get_activity_count(posts, url: str):
    request = requests.get(url)
    if request.status_code == 200: # Because Morgain Stainley is a high proirity client, I have decided to rather send them no data at all, than to send them half-currupted data which could potentially cause monetary loss 
        payload = request.json()    # thus only http responses of a 200 code will be seen as a valid data response
        posts.append(len(payload))
    else:
        posts.append("Unavailable") # The keyword "Unavailable" will be used in the case where the activity count of a given social media can't be retrieved 