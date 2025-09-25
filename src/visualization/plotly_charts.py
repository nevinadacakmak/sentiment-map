import plotly.express as px
import pandas as pd

def create_sentiment_trend_chart(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='date', y='sentiment_score', color='province', title='Sentiment Trend Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Sentiment Score')
    return fig

def create_sentiment_distribution_chart(data):
    df = pd.DataFrame(data)
    fig = px.histogram(df, x='sentiment_score', color='province', title='Sentiment Score Distribution')
    fig.update_layout(xaxis_title='Sentiment Score', yaxis_title='Count')
    return fig

def create_province_comparison_chart(data):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='province', y='average_sentiment', title='Average Sentiment by Province')
    fig.update_layout(xaxis_title='Province', yaxis_title='Average Sentiment')
    return fig