import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple


def perform_clustering(sentiment_df: pd.DataFrame, num_clusters: int = 5) -> Tuple[pd.DataFrame, any]:
    """Perform clustering on sentiment numeric columns and add 'cluster' column to DataFrame.

    Expects columns: ['neg', 'neu', 'pos', 'compound'] or will attempt to use ['compound'].
    Returns (df_with_clusters, cluster_centers)
    """
    df = sentiment_df.copy()
    features = []
    for col in ['neg', 'neu', 'pos', 'compound']:
        if col in df.columns:
            features.append(col)

    if not features:
        raise ValueError('No suitable sentiment numeric columns found for clustering')

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(scaled)

    df['cluster'] = labels
    return df, kmeans.cluster_centers_


def get_clustered_sentiment(sentiment_df: pd.DataFrame) -> pd.DataFrame:
    clustered_data = sentiment_df.groupby('cluster').mean().reset_index()
    return clustered_data