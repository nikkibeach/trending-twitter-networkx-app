### trending-twitter-networkx-app

A simple web application that lets the user visualize connected entities in
Twitter for any of the top 10 trending topics in Germany as well as any other
trends/topics provided by the user in the form of a comma-separated list.

The app was mainly created to get some hands-on experience using the Twitter API
visualizing networks. It was build using Streamlit, Tweepy, NetworkX and pyvis.
It is deployed with Docker on AWS Elastic Beanstalk. You can check it out here:
https://bit.ly/3cZNP5Q

To deploy the application yourself, you will need to have your own Twitter API
credentials, as is shown in the `.env.example` file.
