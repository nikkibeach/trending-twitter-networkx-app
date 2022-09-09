"""Trending on Twitter NetworkX App

This app visualizes connections between entities in Twitter's trending topics
for Germany, making use of the NetworkX and pyvis libraries. It also accepts
user input for additional link analysis.
"""

import os
from collections import Counter

import tweepy
import pandas as pd
import networkx as nx
import streamlit as st
from dotenv import load_dotenv
from pyvis.network import Network

import app_layout  # local module containing layout and text elements


@st.experimental_singleton()
def get_tweepy_api() -> tweepy.api:
    """Authenticate and return tweepy API instance."""
    load_dotenv()  # Take environment variables from .env file
    BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
    auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
    api = tweepy.API(auth)
    return api


@st.experimental_memo(ttl=60 * 5)  # Cache for 5 minutes
def get_trends_list() -> list[str]:
    """Return top 10 trending Twitter topics for Germany."""
    trends = api.get_place_trends(23424829)  # Germany's Yahoo! Where On Earth ID
    trend_names_top10 = [trend["name"] for trend in trends[0]["trends"][1:11]]
    return trend_names_top10


@st.experimental_memo(ttl=60 * 5)  # Cache for 5 minutes
def add_trend_to_df(trend: str) -> pd.DataFrame:
    """Return pandas.DataFrame containing entities for any given `trend`."""
    tweets = api.search_tweets(q=trend, count=100)

    # Loop through sourced tweets and save entities
    hashtags = []
    mentions = []
    for tweet in tweets:
        for tag in tweet.entities["hashtags"]:
            if tag["text"].lower() != trend.replace("#", "").lower():
                hashtags.append(tag["text"])
        for mention in tweet.entities["user_mentions"]:
            mentions.append(mention["name"])

    # Dedupe and count entities
    hashtags = Counter(hashtags)
    mentions = Counter(mentions)

    hashtag_names = list(hashtags.keys())
    mention_names = list(mentions.keys())
    target = hashtag_names + mention_names

    hashtag_counts = list(hashtags.values())
    mention_counts = list(mentions.values())
    value = hashtag_counts + mention_counts

    # Populate pandas.DataFrame with sourced data
    d = {
        "source": [trend.replace("#", "")] * len(target),
        "target": target,
        "type": ["hashtag"] * len(hashtags) + ["mention"] * len(mentions),
        "value": value,
    }
    new_df = pd.DataFrame(data=d)
    return new_df


def draw_network_graph(df):
    """Draw graph of networkx instance."""
    G = nx.from_pandas_edgelist(df, "source", "target", "value")
    trends_net = Network(
        height="410px", width="100%", bgcolor="#0e1117", font_color="white"
    )
    trends_net.from_nx(G)
    trends_net.save_graph("/tmp/graph.html")
    html_file = open("/tmp/graph.html", "r", encoding="utf-8")
    st.components.v1.html(html_file.read(), height=435)


app_layout.setup_page()

api = get_tweepy_api()
trends = get_trends_list()
selected_trends = st.multiselect(
    "Select the Germany trend(s) you are interested in:", trends
)
selected_input = st.text_input(
    "Or try adding trends of your own (as a comma-seperated list):"
)

df = pd.DataFrame(columns=["source", "target", "type", "value"])

for trend in selected_trends:
    new_df = add_trend_to_df(trend)
    df = pd.concat([df, new_df])

if len(selected_trends) > 0:
    draw_network_graph(df[df.value > 1])
