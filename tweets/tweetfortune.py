#!/usr/bin/env python3

# Adapted from https://gist.github.com/yanofsky/5436496

import argparse
import datetime
import logging
import re
import sys

from typing import TextIO

import tweepy


logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
)
LOGGER = logging.getLogger(__name__)


def tweet_is_boring(tweet):
    """Return true if a tweet contains "entities" or properties that don't interest us

    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

    Tweets can contain "entities" like photos, user replies, polls, etc.
    We don't want to bother with tweets containing most types of entities.
    Detect entities here.

    We also are not interested if the tweet is a reply, retweet, a quote tweet, or is truncated.
    """
    for entity_type in ["hashtags", "urls", "user_mentions", "media", "polls"]:
        if entity_type in tweet.entities and tweet.entities[entity_type]:
            LOGGER.info(
                f"Unwanted {entity_type} entity '{tweet.entities[entity_type]}' in tweet ID {tweet.id}: {tweet.full_text}"
            )
            return True
    for prop in ["in_reply_to_user_id", "is_quote_status", "truncated"]:
        # I happen to know that all of those are in __dict__, bleh what a pain
        if tweet.__dict__[prop]:
            LOGGER.info(
                f"Unwanted {prop} property '{getattr(tweet, prop)} in tweet ID {tweet.id}: {tweet.full_text}"
            )
            return True
    return False


double_newline_re = re.compile("\n\n")


def write_tweet_fortune(fp: TextIO, tweet: tweepy.Status):
    """Write a tweet in fortune format

    fp: An open file pointer
    tweet: The tweet to add to the file

    The caller is responsible for opening and closing the fp
    """
    fp.write(f"{tweet.full_text}\n")
    if double_newline_re.search(tweet.full_text):
        # If there is a paragraph break in the tweet,
        # put two newlines before the citation
        fp.write("\n")
    create_date = tweet.created_at.strftime("%B %d, %Y")
    fp.write(f" - @{tweet.user.screen_name} on {create_date}\n")
    fp.write(f"   https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}\n")
    fp.write("%\n")


def get_all_tweets(
    filename: str,
    screen_name: str,
    consumer_key: str,
    consumer_secret: str,
    access_key: str,
    access_secret: str,
):
    """Get all of a user's tweets, and write them to a fortune file

    Skip tweets that have media, are replies/RTs, contain URLs, are part of a tweetstorm, etc.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(
        screen_name=screen_name, count=200, tweet_mode="extended"
    )
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, tweet_mode="extended", max_id=oldest
        )
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")

    # List of tweet IDs which have been replied to
    # Twitter does not allow collecting replies to tweets,
    # but it is easy to see the tweet that a given tweet is in reply to (if any),
    # We want to exclude tweets that start tweetstorms.
    # We get tweets in reverse chrono order,
    # so we can record the IDs of replied-to tweets, and skip them if we encounter them.
    replied_to_tweets = []

    with open(filename, "w") as fp:
        for tweet in alltweets:
            if tweet.in_reply_to_status_id:
                replied_to_tweets.append(tweet.in_reply_to_status_id)
                LOGGER.info(
                    f"Skipping a reply to tweet ID {tweet.in_reply_to_status_id} with ID {tweet.id}: {tweet.full_text}"
                )
                continue
            if tweet.id in replied_to_tweets:
                LOGGER.info(
                    f"Skipping tweet in tweetstorm with ID {tweet.id}: {tweet.full_text}"
                )
                continue
            if tweet_is_boring(tweet):
                continue
            LOGGER.info(f"Saving tweet ID {tweet.id}: {tweet.full_text}")
            write_tweet_fortune(fp, tweet)


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        "Get the most recent 3200 tweets (max allowed from Twitter API) for a user"
    )
    parser.add_argument("--debug", action="store_true", help="Show debug messages")
    parser.add_argument("username", help="Get tweets for this user")
    parser.add_argument(
        "--consumer-key", required=True, help="Twitter API consumer key"
    )
    parser.add_argument(
        "--consumer-secret", required=True, help="Twitter API consumer secret"
    )
    parser.add_argument("--access-key", required=True, help="Twitter API access key")
    parser.add_argument(
        "--access-secret", required=True, help="Twitter API access secret"
    )
    parser.add_argument(
        "--file",
        help="The name of the fortune file to create; USERNAME.DATE.tweets by default",
    )
    parsed = parser.parse_args()

    if parsed.debug:
        LOGGER.setLevel(logging.DEBUG)
    if parsed.file:
        filename = parsed.file
    else:
        today = datetime.datetime.today().strftime("%Y%m%d")
        filename = f"{parsed.username}.{today}.tweets"

    get_all_tweets(
        filename,
        parsed.username,
        parsed.consumer_key,
        parsed.consumer_secret,
        parsed.access_key,
        parsed.access_secret,
    )


if __name__ == "__main__":
    main(sys.argv)
