import unittest
from src.data.reddit_collector import get_reddit_data
from src.data.data_processor import clean_data

class TestRedditDataCollection(unittest.TestCase):

    def test_get_reddit_data(self):
        subreddit = 'toronto'
        data = get_reddit_data(subreddit)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

class TestDataProcessing(unittest.TestCase):

    def test_clean_data(self):
        raw_data = [
            {'title': 'Test Post 1', 'content': 'This is a test content!'},
            {'title': 'Test Post 2', 'content': 'Another test content!'}
        ]
        cleaned_data = clean_data(raw_data)
        self.assertIsInstance(cleaned_data, list)
        self.assertGreater(len(cleaned_data), 0)
        self.assertIn('cleaned_content', cleaned_data[0])

if __name__ == '__main__':
    unittest.main()