import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Step 1: Set up Reddit API access
reddit = praw.Reddit(client_id='Client Id',
                     client_secret='Client Secret',
                     user_agent='User Agent')

# Step 2: Fetch Reddit posts
def fetch_reddit_posts(subreddit_name, post_limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=post_limit):
        posts.append(post.title + ' ' + post.selftext)
    return posts

# Step 3: Perform Sentiment Analysis
def analyze_sentiment(posts):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    total_sentences = 0
    
    for post in posts:
        sentences = post.split('.')
        total_sentences += len(sentences)
        for sentence in sentences:
            score = analyzer.polarity_scores(sentence)
            if score['compound'] >= 0.05:
                sentiments['positive'] += 1
            elif score['compound'] <= -0.05:
                sentiments['negative'] += 1
            else:
                sentiments['neutral'] += 1
    
    # Step 4: Calculate the percentages
    for sentiment in sentiments:
        sentiments[sentiment] = (sentiments[sentiment] / total_sentences) * 100
    
    return sentiments

# Step 5: Plot Sentiment Percentages as a Pie Chart
def plot_sentiment_pie_chart(sentiment_percentages):
    labels = sentiment_percentages.keys()
    sizes = sentiment_percentages.values()
    colors = ['green', 'red', 'grey']
    explode = (0.1, 0, 0)  # explode the 1st slice (positive)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Sentiment Analysis of Reddit Posts')
    plt.show()

# Example usage
subreddit_name = 'A Reddit Page'  # Replace with the subreddit you want to analyze
posts = fetch_reddit_posts(subreddit_name, post_limit=100)
sentiment_percentages = analyze_sentiment(posts)

print(f"Sentiment analysis for /r/{subreddit_name}:")
print(f"Positive: {sentiment_percentages['positive']:.2f}%")
print(f"Negative: {sentiment_percentages['negative']:.2f}%")
print(f"Neutral: {sentiment_percentages['neutral']:.2f}%")

# Plot the pie chart
plot_sentiment_pie_chart(sentiment_percentages)
