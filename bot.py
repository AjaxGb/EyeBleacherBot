import random
import config
import praw
import time

TRIGGERS = [
    "unsee juice",
    "i need bleach",
    "who's got the bleach",
    "where's the bleach",
    "bleach my eyes",
    "bleach please",
    "get the bleach",
    "i need eyebleach",
    "give me bleach",
    "give me the bleach",
    "i need the bleach",
    "i need eye bleach",
    "wheres the bleach",
    "i need some bleach",
    "who's got the bleach",
    "need eye bleach",
    "have eyebleach",
    "pour the bleach",
    "pour me some bleach",
    "eyebleach needed",
    "who has the bleach",
    "eyebleach please",
    "gimme the bleach",
]


def authenticate():
    reddit = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
    )
    return reddit


def getReplies():
    with open("replies.txt", "r") as file:
        cr = file.read()
        cr2 = list(cr)
        cr2 = cr2
        cr = cr
        cr = cr.split("\n")
        cr = filter(None, cr)
    return cr


def run(reddit, cr2):

    with open("bleach.txt") as b, open("subs.txt", "r") as subs, open(
        "footer.txt", "r"
    ) as footer:

        a = b.readlines()

    for comment in reddit.subreddit(subs).stream.comments(skip_existing=True):

        if (
            "!eyebleacherbot" in comment.body.lower()
            or "u/eyebleacherbot" in comment.body.lower()
            and comment.id not in cr2
            and not comment.saved
        ):
            try:

                print("Bot called")
                comment.save()
                comment.reply(random.choice(a) + "\n" + footer)
                print("Bot replied")
                list(cr2).append(comment.id)

                with open("replies.txt", "a") as file:
                    file.write(comment.id + "\n")

            except Exception as e:
                print(e)
                time.sleep(30)

        if (
            any(e in comment.body.lower() for e in TRIGGERS)
            and comment.id not in cr2
            and not comment.saved
        ):

            try:

                print("Bot called")
                comment.save()
                comment.reply(random.choice(a) + footer)
                print("Bot replied")
                list(cr2).append(comment.id)

                with open("replies.txt", "a") as file:
                    file.write(comment.id + "\n")

            except Exception as e:
                print(e)
                time.sleep(30)

        elif (
            "[nsfl]" in comment.body.lower()
            and comment.id not in cr2
            and not comment.saved
        ):
            try:

                print("Bot called")
                comment.save()
                comment.reply(
                    "*Not Safe for Life content detected!*"
                    + "\n\n"
                    + random.choice(a)
                    + footer
                )
                print("Bot replied")
                list(cr2).append(comment.id)

                with open("replies.txt", "a") as file:
                    file.write(comment.id + "\n")

            except Exception as e:
                print(e)
                time.sleep(30)

    time.sleep(60)
