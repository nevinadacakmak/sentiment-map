import yaml
import json
from dotenv import load_dotenv
import os

from data.reddit_collector import collect_reddit_data
from data.data_processor import process_data
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.clustering import perform_clustering
from database.mongodb_client import MongoDBClient
from visualization.dashboard import run_dashboard


def main():
    # Load environment variables from .env (if present)
    load_dotenv()

    # Load configuration (YAML)
    with open('config/config.yaml') as config_file:
        config = yaml.safe_load(config_file)

    # Initialize MongoDB client
    mongo_uri = config.get('mongo_uri') or os.getenv('MONGODB_URI')
    db_name = config.get('database_name')
    collection_name = config.get('collection_name', 'reddit_posts')

    mongo_client = MongoDBClient(mongo_uri, db_name)

    # Collect data from Reddit for configured provinces/subreddits
    provinces = config.get('provinces', [])
    subreddit_data = collect_reddit_data(provinces, limit=50)

    # Process the collected data
    processed_df = process_data(subreddit_data)

    # Analyze sentiment
    analyzer = SentimentAnalyzer()
    sentiment_df = analyzer.analyze_sentiments_in_dataframe(processed_df, 'content')

    # Perform clustering on sentiment data (adds 'cluster' column)
    clustered_df, cluster_centers = perform_clustering(sentiment_df)

    # Store data in MongoDB
    mongo_client.store_data(collection_name, clustered_df)

    # Run the Plotly Dash dashboard (opens web server)
    # Optionally provide a GeoJSON file path and feature id key for choropleth
    geojson_path = config.get('geojson_path') or os.getenv('CANADA_GEOJSON_PATH')
    featureidkey = config.get('featureidkey') or os.getenv('GEOJSON_FEATUREIDKEY', 'properties.name')
    run_dashboard(mongo_uri, db_name, collection_name, geojson_path=geojson_path, featureidkey=featureidkey)


if __name__ == '__main__':
    main()