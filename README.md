# Sentiment Map Project

## Overview
The Sentiment Map project is a sentiment analysis platform that tracks and visualizes public mood across Canadian provinces using data collected from Reddit. The project utilizes various technologies including Python, BeautifulSoup, VADER for sentiment analysis, MongoDB for data storage, and Plotly Dash for visualization.

## Project Structure
```
sentiment-map
├── src
│   ├── data
│   │   ├── __init__.py
│   │   ├── reddit_collector.py
│   │   └── data_processor.py
│   ├── analysis
│   │   ├── __init__.py
│   │   ├── sentiment_analyzer.py
│   │   └── clustering.py
│   ├── database
│   │   ├── __init__.py
│   │   └── mongodb_client.py
│   ├── visualization
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   └── plotly_charts.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── config
│   ├── config.yaml
│   └── provinces.json
├── notebooks
│   └── exploratory_analysis.ipynb
├── tests
│   ├── __init__.py
│   ├── test_data.py
│   └── test_analysis.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Features
- **Data Collection**: Collects data from Reddit using the Reddit API.
- **Data Processing**: Cleans and preprocesses the collected data for analysis.
- **Sentiment Analysis**: Analyzes sentiment using the VADER sentiment analysis tool.
- **Clustering**: Applies unsupervised clustering to detect trends in sentiment data.
- **Visualization**: Visualizes sentiment trends and distributions using Plotly Dash.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd sentiment-map
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Update the `config/config.yaml` file with your API keys and MongoDB connection details.
   - Modify `config/provinces.json` to include relevant subreddits for each Canadian province.

4. **Run the Application**:
   Execute the main script to start the data collection and visualization process:
   ```
   python src/main.py
   ```

## Usage
- The application will collect data from specified subreddits, process the data, perform sentiment analysis, and visualize the results in a web dashboard.
- Access the dashboard in your web browser at `http://127.0.0.1:8050`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.