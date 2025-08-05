import praw
import os
from textblob import TextBlob
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RedditService:
    """
    Service for fetching and analyzing Reddit reviews for AI tools
    """
    
    def __init__(self):
        """Initialize Reddit API client"""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'InsightEngine/1.0')
        )
        
    def search_reviews(self, tool_name: str, subreddits: List[str] = None) -> List[Dict]:
        """
        Search for reviews of a specific AI tool across Reddit
        
        Args:
            tool_name: Name of the AI tool to search for
            subreddits: List of subreddits to search in (default: AI-related subreddits)
            
        Returns:
            List of review dictionaries with sentiment analysis
        """
        if subreddits is None:
            subreddits = [
                'artificial', 'MachineLearning', 'datascience', 
                'programming', 'technology', 'startups',
                'ChatGPT', 'OpenAI', 'AI', 'artificialintelligence'
            ]
        
        reviews = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Search for posts about the tool
                search_query = f"{tool_name}"
                posts = subreddit.search(search_query, sort='relevance', time_filter='year', limit=50)
                
                for post in posts:
                    # Analyze the post title and content
                    title_sentiment = self._analyze_sentiment(post.title)
                    content_sentiment = self._analyze_sentiment(post.selftext) if post.selftext else None
                    
                    # Get comments
                    post.comments.replace_more(limit=0)  # Remove MoreComments objects
                    comments = []
                    
                    for comment in post.comments.list()[:10]:  # Top 10 comments
                        comment_sentiment = self._analyze_sentiment(comment.body)
                        comments.append({
                            'body': comment.body,
                            'score': comment.score,
                            'sentiment': comment_sentiment,
                            'created_utc': comment.created_utc
                        })
                    
                    reviews.append({
                        'title': post.title,
                        'content': post.selftext,
                        'url': f"https://reddit.com{post.permalink}",
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'created_utc': post.created_utc,
                        'title_sentiment': title_sentiment,
                        'content_sentiment': content_sentiment,
                        'comments': comments,
                        'subreddit': subreddit_name
                    })
                    
            except Exception as e:
                logger.error(f"Error searching subreddit {subreddit_name}: {e}")
                continue
        
        return reviews
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using TextBlob
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with polarity, subjectivity, and sentiment label
        """
        if not text or len(text.strip()) < 10:
            return {
                'polarity': 0,
                'subjectivity': 0,
                'sentiment': 'neutral'
            }
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment
        }
    
    def aggregate_reviews(self, reviews: List[Dict]) -> Dict:
        """
        Aggregate review data to create summary statistics
        
        Args:
            reviews: List of review dictionaries
            
        Returns:
            Dictionary with aggregated review data
        """
        if not reviews:
            return None
        
        # Calculate overall sentiment
        total_polarity = 0
        total_subjectivity = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        # Collect positive and negative feedback
        positive_feedback = []
        negative_feedback = []
        
        for review in reviews:
            # Title sentiment
            if review['title_sentiment']['sentiment'] == 'positive':
                positive_count += 1
                positive_feedback.append(review['title'])
            elif review['title_sentiment']['sentiment'] == 'negative':
                negative_count += 1
                negative_feedback.append(review['title'])
            else:
                neutral_count += 1
            
            # Content sentiment
            if review['content_sentiment']:
                if review['content_sentiment']['sentiment'] == 'positive':
                    positive_count += 1
                    positive_feedback.append(review['content'][:200] + "...")
                elif review['content_sentiment']['sentiment'] == 'negative':
                    negative_count += 1
                    negative_feedback.append(review['content'][:200] + "...")
                else:
                    neutral_count += 1
            
            total_polarity += review['title_sentiment']['polarity']
            total_subjectivity += review['title_sentiment']['subjectivity']
            
            if review['content_sentiment']:
                total_polarity += review['content_sentiment']['polarity']
                total_subjectivity += review['content_sentiment']['subjectivity']
        
        # Calculate averages
        total_reviews = len(reviews) * 2  # Title + content
        avg_polarity = total_polarity / total_reviews if total_reviews > 0 else 0
        avg_subjectivity = total_subjectivity / total_reviews if total_reviews > 0 else 0
        
        # Convert polarity to 0-5 rating scale
        overall_rating = (avg_polarity + 1) * 2.5  # Convert from -1,1 to 0,5 scale
        overall_rating = max(0, min(5, overall_rating))  # Clamp to 0-5
        
        return {
            'overall_rating': round(overall_rating, 1),
            'ease_of_use_score': round(overall_rating * 0.9, 1),  # Slightly lower
            'feature_score': round(overall_rating * 1.1, 1),  # Slightly higher
            'value_for_money_score': round(overall_rating * 0.8, 1),  # Lower for value
            'positive_sentiment_summary': self._summarize_feedback(positive_feedback[:5]),
            'negative_sentiment_summary': self._summarize_feedback(negative_feedback[:5]),
            'total_reviews': len(reviews),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'avg_polarity': round(avg_polarity, 3),
            'avg_subjectivity': round(avg_subjectivity, 3)
        }
    
    def _summarize_feedback(self, feedback_list: List[str]) -> str:
        """
        Create a summary of feedback points
        
        Args:
            feedback_list: List of feedback strings
            
        Returns:
            Summarized feedback string
        """
        if not feedback_list:
            return "No specific feedback available."
        
        # Take the most common themes (simplified approach)
        if len(feedback_list) <= 3:
            return " ".join(feedback_list)
        else:
            return " ".join(feedback_list[:3]) + "..." 