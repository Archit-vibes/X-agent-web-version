from auth.storage import user_tokens
from flask import session
from datetime import datetime
from xdk import Client

def fetch_recent_mentions(id):
    # user_id = session["user_id"]
    # token = user_tokens[user_id]["access_token"]

    # client = Client(bearer_token=token)

    # print(f"[{datetime.now():%H:%M:%S}] Requesting first page for mentions")
    # iterator = client.users.get_mentions(id=id , max_results=10 , tweet_fields=["id" , "author_id"])
    # first_page = next(iterator)

    # mentions = first_page.data or []

    print(id)

    psuedo_mentions = [{'text': '@Mridulchdry The bar for corporate culture is so low in Indian orgs that giving people space and time for personal things is considered a lucky thing thankfully I started working in an eu org.', 'author_id': '1519690915274579968', 'id': '2014745001289474226', 'edit_history_tweet_ids': ['2014745001289474226']}, {'text': '@Mridulchdry Ab party dede bhai', 'author_id': '1411598581920718860', 'id': '2014721752069439492', 'edit_history_tweet_ids': ['2014721752069439492']}, {'text': '@Mridulchdry Jay Shah writing scripts with Gemini lessss goooooooo', 'author_id': '1501352893651116033', 'id': '2014244086220537871', 'edit_history_tweet_ids': ['2014244086220537871']}, {'text': 'me and @Mridulchdry tryna take a workshop or to like build a community in our cllgs.\nmore than 80 folks have already joined the WA grp and i can bet not even half would show up.', 'author_id': '1411598581920718860', 'id': '2014043442570023339', 'edit_history_tweet_ids': ['2014043442570023339']}]

    return psuedo_mentions