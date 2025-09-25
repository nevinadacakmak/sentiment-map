from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from typing import Optional
from database.mongodb_client import MongoDBClient
import os
import json


# Basic centroid mapping for Canadian provinces (lat, lon) - simplified
PROVINCE_CENTROIDS = {
    'Alberta': {'lat': 53.9333, 'lon': -116.5765},
    'British Columbia': {'lat': 53.7267, 'lon': -127.6476},
    'Manitoba': {'lat': 53.7609, 'lon': -98.8139},
    'New Brunswick': {'lat': 46.5653, 'lon': -66.4619},
    'Newfoundland and Labrador': {'lat': 53.1355, 'lon': -57.6604},
    'Nova Scotia': {'lat': 44.6820, 'lon': -63.7443},
    'Ontario': {'lat': 51.2538, 'lon': -85.3232},
    'Prince Edward Island': {'lat': 46.5107, 'lon': -63.4168},
    'Quebec': {'lat': 52.9399, 'lon': -73.5491},
    'Saskatchewan': {'lat': 52.9399, 'lon': -106.4509}
}


def run_dashboard(mongo_uri: str,
                  db_name: str,
                  collection_name: str,
                  host: str = '127.0.0.1',
                  port: int = 8050,
                  geojson_path: Optional[str] = None,
                  featureidkey: str = 'properties.name'):
    app = Dash(__name__)

    # Fetch data from MongoDB
    mongo_client = MongoDBClient(mongo_uri, db_name)
    records = mongo_client.get_sentiment_data(collection_name)
    if not records:
        df = pd.DataFrame(columns=['province', 'compound'])
    else:
        df = pd.DataFrame(records)

    # Aggregate by province
    if 'province' in df.columns and 'compound' in df.columns:
        agg = df.groupby('province')['compound'].mean().reset_index()
    else:
        agg = pd.DataFrame(columns=['province', 'compound'])

    # If a geojson is provided and exists, try to render a choropleth
    if geojson_path:
        try:
            if os.path.exists(geojson_path):
                with open(geojson_path, 'r', encoding='utf-8') as fh:
                    geojson = json.load(fh)

                # locations must match the feature property referenced by featureidkey
                # e.g., featureidkey='properties.name' and agg['province'] contains matching names
                fig = px.choropleth_mapbox(agg,
                                           geojson=geojson,
                                           locations='province',
                                           color='compound',
                                           featureidkey=featureidkey,
                                           hover_name='province',
                                           color_continuous_scale=px.colors.sequential.Plasma,
                                           mapbox_style='open-street-map',
                                           center={'lat': 56.1304, 'lon': -106.3468},
                                           zoom=3,
                                           height=600)
                fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
            else:
                raise FileNotFoundError(f'GeoJSON not found at {geojson_path}')
        except Exception:
            # Fall back to centroid scatter map if geojson plotting fails
            lats = []
            lons = []
            for prov in agg['province']:
                centroid = PROVINCE_CENTROIDS.get(prov, {'lat': None, 'lon': None})
                lats.append(centroid['lat'])
                lons.append(centroid['lon'])

            agg['lat'] = lats
            agg['lon'] = lons
            fig = px.scatter_mapbox(agg.dropna(subset=['lat', 'lon']),
                                    lat='lat', lon='lon', size='compound', color='compound', hover_name='province',
                                    color_continuous_scale=px.colors.sequential.Plasma, zoom=3, height=600)
            fig.update_layout(mapbox_style='open-street-map')
    else:
        # Map centroids when no geojson provided
        lats = []
        lons = []
        for prov in agg['province']:
            centroid = PROVINCE_CENTROIDS.get(prov, {'lat': None, 'lon': None})
            lats.append(centroid['lat'])
            lons.append(centroid['lon'])

        agg['lat'] = lats
        agg['lon'] = lons

        fig = px.scatter_mapbox(agg.dropna(subset=['lat', 'lon']),
                                lat='lat', lon='lon', size='compound', color='compound', hover_name='province',
                                color_continuous_scale=px.colors.sequential.Plasma, zoom=3, height=600)
        fig.update_layout(mapbox_style='open-street-map')

    app.layout = html.Div(children=[
        html.H1(children='Sentiment Analysis Dashboard'),
        dcc.Graph(id='sentiment-map', figure=fig)
    ])

    app.run_server(host=host, port=port, debug=True)


if __name__ == '__main__':
    # Allow running locally with default env values
    import os
    run_dashboard(os.getenv('MONGODB_URI'), os.getenv('MONGODB_DB'), os.getenv('MONGODB_COLLECTION', 'reddit_posts'))