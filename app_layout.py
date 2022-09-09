"""This module contains the app's text and layout elements. """

import streamlit as st


def setup_page() -> None:
    """Set the application's general appearance."""
    st.set_page_config(page_title="Trending on Twitter Network App", page_icon="🐦")
    st.title("Twitter's Trending Topics for Germany")
    st.markdown(
        """This application lets you visualize networks of connected entities in
        Twitter's trending topics for Germany. The top ten trending topics right
        now are provided, but you can also add queries of your own. The source code
        is available on
        [GitHub](https://github.com/nikkibeach/trending-twitter-networkx-app).
    """
    )
    st.markdown(
        """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """,
        unsafe_allow_html=True,
    )
