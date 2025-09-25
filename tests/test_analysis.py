import unittest
from src.analysis.sentiment_analyzer import analyze_sentiment
from src.analysis.clustering import perform_clustering

class TestSentimentAnalysis(unittest.TestCase):

    def test_analyze_sentiment_positive(self):
        text = "I love the beautiful scenery in Canada!"
        sentiment_score = analyze_sentiment(text)
        self.assertGreater(sentiment_score['compound'], 0)

    def test_analyze_sentiment_negative(self):
        text = "I hate the cold weather in winter."
        sentiment_score = analyze_sentiment(text)
        self.assertLess(sentiment_score['compound'], 0)

    def test_perform_clustering(self):
        sample_data = [
            {'text': "I love the beautiful scenery in Canada!", 'sentiment': 0.8},
            {'text': "I hate the cold weather in winter.", 'sentiment': -0.6},
            {'text': "The food in Toronto is amazing!", 'sentiment': 0.9},
            {'text': "I dislike the traffic in Vancouver.", 'sentiment': -0.5}
        ]
        clusters = perform_clustering(sample_data)
        self.assertIsInstance(clusters, list)
        self.assertGreater(len(clusters), 0)

if __name__ == '__main__':
    unittest.main()