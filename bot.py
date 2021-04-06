from threading import Thread
from time import sleep
from random import choice
import functools
import traceback
import logging
import config
import praw
import json

TRIGGERS = [
    "!eyebleacherbot",
    "i need bleach",
    "unsee juice",
    "the bleach",
    "bleach my eyes",
    "bleach please",
    "i need eyebleach",
    "give me bleach",
    "i need eye bleach",
    "i need some bleach",
    "i need some eye bleach",
    "need eye bleach",
    "any bleach",
    "bleach my eyes",
    "eyebleach bot",
    "day to have eyes",
    "unsee bot",
    "bleach bot",
    "r/eyebleach",
    "juice of unseeing",
]


def authenticate():
    """
    authenticate the bot
    """
    reddit = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    return reddit


def log(message):
    """
    log all comments deleted for a bad vote or score   
    """
    logging.basicConfig(level=logging.INFO, filename='bot.log', format='%(asctime)s %(levelname)s:%(message)s')
    
    try:

        logging.info(message)

    except Exception:
        print(traceback.format_exc())

               

def send_bleach(method):
    """
    reply with randomly selected bleach given a certain method
    """
    try:

        with open("bleach.txt") as b:
            bl = b.readlines()
            msg = " \n*^(beep)* *^(boop! I'm a bot! Please contact)* [*^(u/cyanidesuppository)*](https://reddit.com/user/cyanidesuppository) *^(with)* *^(any)* *^(issues)* *^(or)* *^(suggestions!) *^(|)* [*^(Github)*](https://github.com/getcake/eyebleacherbot)*"
            bleach = choice(bl) + "\n" + msg
            method.reply(bleach)

        return bleach

    except Exception:
        print(traceback.format_exc())


def get_user_mentions(reddit):
    """
    stream generator for unread inbox mentions
    """
    for mention in praw.models.util.stream_generator(reddit.inbox.unread):
        try:

            if "u/eyebleacherbot" in mention.body.lower():
                print("Bot called by username mention")
                send_bleach(mention)
                mention.mark_read()
                print("Bot responded to username mention\n")

        except Exception:
            print(traceback.format_exc())


def keep_score(reddit):
    """
    keep track of all comment scores and deletes ones under a certain threshold
    """
    for comment in reddit.redditor("eyebleacherbot").stream.comments():
        try:

            score = comment.score
            threshold = - 1
            if score < threshold:
                comment.delete()
                print(f"Comment deleted at threshold: {threshold}\n")
                log(message=f'Comment was deleted for being under threshold: {threshold}')

        except Exception:
            print(traceback.format_exc())


def be_good(reddit):
    """
    delete comments that have recieved a bad vote
    """
    for reply in praw.models.util.stream_generator(reddit.inbox.comment_replies):
        try:

            og = reply.parent()
            author = reply.author
            bad_vote = 'bad bot'
            bad_comment = reply.body
            if bad_vote in bad_comment.lower():
                print("Found bad vote")
                og.delete()
                print(f'Comment was delted because of bad vote by u/{author} [COMMENT]: "{bad_comment}" ')
                log(message=f'Comment was delted because of bad vote by u/{author} [COMMENT]: "{bad_comment}" ')

        except Exception:
            print(traceback.format_exc())


def search_triggers(reddit):
    """
    search for any occurance of a trigger in the list "TRIGGERS"
    """
    for comment in reddit.subreddit("subs go here").stream.comments(
        skip_existing=True
    ):
        try:

            if any(e in comment.body.lower() for e in TRIGGERS):
                print("Bot called by trigger")
                comment.save()
                send_bleach(comment)
                print("Bot replied to trigger\n")

        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    try:
        reddit = authenticate()
        Thread(target=functools.partial(search_triggers, reddit)).start()
        print("[*]  Searching for triggers")
        Thread(target=functools.partial(get_user_mentions, reddit)).start()
        print("[*]  Getting username mentions")
        Thread(target=functools.partial(be_good, reddit)).start()
        print("[*]  Being good")
        Thread(target=functools.partial(keep_score, reddit)).start()
        print("[*]  Keeping score\n")

    except Exception:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
        sleep(30)
