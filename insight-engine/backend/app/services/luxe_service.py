import praw
import os
from textblob import TextBlob
from typing import List, Dict, Optional
import logging
import random
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LuxeService:
    def __init__(self):
        self.has_credentials = bool(os.getenv('REDDIT_CLIENT_ID') and os.getenv('REDDIT_CLIENT_SECRET'))
        if self.has_credentials:
            self.reddit = praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent=os.getenv('REDDIT_USER_AGENT', 'InsightEngine/1.0')
            )
        else:
            logger.warning("Reddit credentials not configured. Using demo mode.")
            self.reddit = None

    def search_reviews(self, appliance_name: str, brand: str) -> List[Dict]:
        """Search for luxury appliance reviews with design and renovation context"""
        if not self.has_credentials:
            return self._get_demo_reviews(appliance_name, brand)

        # Subreddits focused on home renovation, design, and luxury
        subreddits = [
            'HomeImprovement', 'InteriorDesign', 'kitchenporn', 
            'luxuryhomes', 'architecture', 'homeowners',
            'Appliances', 'KitchenDesign', 'Renovations'
        ]

        reviews = []
        search_terms = [
            f'"{brand}" "{appliance_name}"',
            f'"{brand}" review',
            f'"{appliance_name}" review',
            f'"{brand}" kitchen',
            f'"{brand}" appliance'
        ]

        for search_query in search_terms:
            for subreddit_name in subreddits:
                try:
                    logger.info(f"Searching {subreddit_name} for: {search_query}")
                    subreddit = self.reddit.subreddit(subreddit_name)
                    posts = subreddit.search(search_query, sort='relevance', time_filter='year', limit=8)

                    for post in posts:
                        if post.score < 3:  # Quality filter
                            continue

                        # Analyze post content
                        post_review = self._analyze_luxe_review(
                            post.title + " " + post.selftext,
                            post.author.name if post.author else "Anonymous",
                            post.created_utc,
                            post.score,
                            post.url,
                            appliance_name,
                            brand
                        )
                        if post_review:
                            reviews.append(post_review)

                        # Get top comments
                        post.comments.replace_more(limit=0)
                        for comment in post.comments.list()[:5]:
                            if comment.score > 2:
                                comment_review = self._analyze_luxe_review(
                                    comment.body,
                                    comment.author.name if comment.author else "Anonymous",
                                    comment.created_utc,
                                    comment.score,
                                    post.url,
                                    appliance_name,
                                    brand
                                )
                                if comment_review:
                                    reviews.append(comment_review)

                        if len(reviews) >= 12:  # Early stopping
                            break

                except Exception as e:
                    logger.error(f"Error searching subreddit {subreddit_name}: {e}")
                    continue

                time.sleep(0.5)  # Small delay

        return reviews

    def _analyze_luxe_review(self, text: str, author: str, created_utc: int, score: int, url: str, appliance_name: str, brand: str) -> Optional[Dict]:
        """Analyze luxury appliance review with design and renovation context"""
        if not text or len(text.strip()) < 20:
            return None

        # Basic sentiment analysis
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        # Determine reviewer type based on content
        reviewer_type = self._determine_reviewer_type(text)
        
        # Extract renovation context
        renovation_context = self._extract_renovation_context(text)
        
        # Extract design insights
        design_insights = self._extract_design_insights(text)
        
        # Extract ratings
        ratings = self._extract_ratings(text)
        
        # Generate summaries
        positive_summary = self._generate_positive_summary(text) if sentiment > 0.1 else None
        negative_summary = self._generate_negative_summary(text) if sentiment < -0.1 else None

        return {
            'source': 'Reddit',
            'review_date': datetime.fromtimestamp(created_utc),
            'reviewer_type': reviewer_type,
            'renovation_context': renovation_context,
            'design_insights': design_insights,
            'overall_rating': ratings.get('overall'),
            'design_rating': ratings.get('design'),
            'functionality_rating': ratings.get('functionality'),
            'value_rating': ratings.get('value'),
            'positive_sentiment_summary': positive_summary,
            'negative_sentiment_summary': negative_summary,
            'design_trends': self._extract_design_trends_from_text(text),
            'competitor_comparison': self._extract_competitor_mentions_from_text(text),
            'price_sentiment': self._extract_price_sentiment(text),
            'installation_insights': self._extract_installation_insights(text),
            'raw_review_text': text[:1000],  # Limit text length
            'search_time': time.time()
        }

    def _determine_reviewer_type(self, text: str) -> str:
        """Determine the type of reviewer based on content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['architect', 'designer', 'interior designer']):
            return 'Designer/Architect'
        elif any(word in text_lower for word in ['contractor', 'builder', 'construction']):
            return 'Contractor'
        elif any(word in text_lower for word in ['renovation', 'remodel', 'kitchen remodel']):
            return 'Homeowner (Renovation)'
        elif any(word in text_lower for word in ['new home', 'new construction', 'building']):
            return 'Homeowner (New Build)'
        else:
            return 'Homeowner'

    def _extract_renovation_context(self, text: str) -> str:
        """Extract kitchen renovation context"""
        text_lower = text.lower()
        context_parts = []
        
        # Kitchen style
        if 'modern' in text_lower:
            context_parts.append('Modern kitchen design')
        elif 'traditional' in text_lower:
            context_parts.append('Traditional kitchen design')
        elif 'contemporary' in text_lower:
            context_parts.append('Contemporary kitchen design')
        elif 'farmhouse' in text_lower:
            context_parts.append('Farmhouse kitchen design')
        
        # Renovation scope
        if 'full kitchen' in text_lower or 'complete renovation' in text_lower:
            context_parts.append('Full kitchen renovation')
        elif 'appliance upgrade' in text_lower or 'replacing appliances' in text_lower:
            context_parts.append('Appliance upgrade only')
        
        # Budget context
        if any(word in text_lower for word in ['luxury', 'high-end', 'premium']):
            context_parts.append('Luxury budget')
        elif any(word in text_lower for word in ['budget', 'cost-effective', 'affordable']):
            context_parts.append('Budget-conscious')
        
        return '; '.join(context_parts) if context_parts else 'Standard kitchen renovation'

    def _extract_design_insights(self, text: str) -> str:
        """Extract design-related insights"""
        text_lower = text.lower()
        insights = []
        
        # Design preferences
        if 'stainless steel' in text_lower:
            insights.append('Prefers stainless steel finish')
        elif 'panel ready' in text_lower or 'integrated' in text_lower:
            insights.append('Interested in panel-ready/integrated design')
        elif 'color' in text_lower or 'colored' in text_lower:
            insights.append('Interested in colored appliances')
        
        # Layout preferences
        if 'island' in text_lower:
            insights.append('Kitchen island configuration')
        if 'open concept' in text_lower:
            insights.append('Open concept kitchen')
        
        # Style preferences
        if 'minimalist' in text_lower or 'clean lines' in text_lower:
            insights.append('Minimalist design preference')
        elif 'statement piece' in text_lower or 'showpiece' in text_lower:
            insights.append('Views appliance as statement piece')
        
        return '; '.join(insights) if insights else 'Standard design preferences'

    def _extract_ratings(self, text: str) -> Dict[str, float]:
        """Extract ratings from text"""
        ratings = {}
        text_lower = text.lower()
        
        # Look for rating patterns
        import re
        rating_patterns = [
            r'(\d+)/5', r'(\d+) out of 5', r'(\d+) stars',
            r'rating[:\s]*(\d+)', r'score[:\s]*(\d+)'
        ]
        
        for pattern in rating_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                rating = float(matches[0])
                if 1 <= rating <= 5:
                    ratings['overall'] = rating
                    break
        
        # Estimate design rating based on design-related keywords
        design_keywords = ['beautiful', 'stunning', 'gorgeous', 'elegant', 'sleek', 'modern', 'design']
        design_score = sum(1 for word in design_keywords if word in text_lower)
        if design_score > 0:
            ratings['design'] = min(5.0, 3.0 + (design_score * 0.5))
        
        # Estimate functionality rating
        functionality_keywords = ['works great', 'excellent performance', 'reliable', 'efficient', 'powerful']
        functionality_score = sum(1 for word in functionality_keywords if word in text_lower)
        if functionality_score > 0:
            ratings['functionality'] = min(5.0, 3.0 + (functionality_score * 0.5))
        
        # Estimate value rating
        value_keywords = ['worth it', 'good value', 'expensive', 'overpriced', 'reasonable']
        value_score = sum(1 for word in value_keywords if word in text_lower)
        if value_score > 0:
            ratings['value'] = min(5.0, 3.0 + (value_score * 0.3))
        
        return ratings

    def _extract_design_trends_from_text(self, text: str) -> str:
        """Extract design trends mentioned in text"""
        text_lower = text.lower()
        trends = []
        
        # Current design trends
        if 'matte black' in text_lower:
            trends.append('Matte black finish trend')
        if 'panel ready' in text_lower:
            trends.append('Panel-ready appliance trend')
        if 'smart features' in text_lower or 'wifi' in text_lower:
            trends.append('Smart appliance integration')
        if 'induction' in text_lower:
            trends.append('Induction cooking trend')
        if 'steam' in text_lower:
            trends.append('Steam cooking features')
        
        return '; '.join(trends) if trends else 'Standard design features'

    def _extract_competitor_mentions_from_text(self, text: str) -> str:
        """Extract mentions of competitor brands"""
        competitors = ['Sub Zero', 'Wolf', 'Cove', 'Thermador', 'Viking', 'Fisher and Paykel', 
                      'Monogram', 'SKS', 'JennAir', 'Gaggenau', 'Bosch', 'Miele', 'KitchenAid']
        
        mentions = []
        text_lower = text.lower()
        
        for competitor in competitors:
            if competitor.lower() in text_lower:
                mentions.append(competitor)
        
        return '; '.join(mentions) if mentions else 'No competitor mentions'

    def _extract_price_sentiment(self, text: str) -> str:
        """Extract price-related sentiment"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['expensive', 'overpriced', 'too much']):
            return 'Negative price sentiment'
        elif any(word in text_lower for word in ['worth it', 'good value', 'reasonable']):
            return 'Positive price sentiment'
        elif any(word in text_lower for word in ['luxury', 'premium', 'investment']):
            return 'Luxury positioning accepted'
        else:
            return 'Neutral price sentiment'

    def _extract_installation_insights(self, text: str) -> str:
        """Extract installation-related insights"""
        text_lower = text.lower()
        insights = []
        
        if 'installation' in text_lower or 'install' in text_lower:
            insights.append('Installation process mentioned')
        if 'professional' in text_lower and 'install' in text_lower:
            insights.append('Professional installation required')
        if 'DIY' in text_lower or 'do it yourself' in text_lower:
            insights.append('DIY installation attempted')
        if 'plumbing' in text_lower or 'electrical' in text_lower:
            insights.append('Plumbing/electrical considerations')
        
        return '; '.join(insights) if insights else 'Standard installation'

    def _generate_positive_summary(self, text: str) -> str:
        """Generate positive sentiment summary"""
        positive_keywords = ['love', 'amazing', 'excellent', 'perfect', 'beautiful', 'stunning', 'great', 'fantastic']
        found_positive = [word for word in positive_keywords if word in text.lower()]
        
        if found_positive:
            return f"Positive feedback focuses on: {', '.join(found_positive[:3])}"
        return "Generally positive sentiment"

    def _generate_negative_summary(self, text: str) -> str:
        """Generate negative sentiment summary"""
        negative_keywords = ['hate', 'terrible', 'awful', 'disappointed', 'problem', 'issue', 'broken', 'expensive']
        found_negative = [word for word in negative_keywords if word in text.lower()]
        
        if found_negative:
            return f"Concerns include: {', '.join(found_negative[:3])}"
        return "Some negative feedback"

    def _extract_design_trends(self, reviews: List) -> Dict:
        """Extract design trends from multiple reviews"""
        trends = {}
        for review in reviews:
            if review.design_trends:
                for trend in review.design_trends.split(';'):
                    trend = trend.strip()
                    trends[trend] = trends.get(trend, 0) + 1
        return trends

    def _extract_competitor_mentions(self, reviews: List) -> Dict:
        """Extract competitor mentions from multiple reviews"""
        mentions = {}
        for review in reviews:
            if review.competitor_comparison:
                for competitor in review.competitor_comparison.split(';'):
                    competitor = competitor.strip()
                    mentions[competitor] = mentions.get(competitor, 0) + 1
        return mentions

    def _extract_price_insights(self, reviews: List) -> Dict:
        """Extract price insights from multiple reviews"""
        insights = {}
        for review in reviews:
            if review.price_sentiment:
                insights[review.price_sentiment] = insights.get(review.price_sentiment, 0) + 1
        return insights

    def _extract_installation_insights(self, reviews: List) -> Dict:
        """Extract installation insights from multiple reviews"""
        insights = {}
        for review in reviews:
            if review.installation_insights:
                for insight in review.installation_insights.split(';'):
                    insight = insight.strip()
                    insights[insight] = insights.get(insight, 0) + 1
        return insights

    def _get_demo_reviews(self, appliance_name: str, brand: str) -> List[Dict]:
        """Generate demo reviews for testing"""
        demo_reviews = [
            {
                'source': 'Reddit',
                'review_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'reviewer_type': 'Homeowner (Renovation)',
                'renovation_context': 'Full kitchen renovation; Modern kitchen design; Luxury budget',
                'design_insights': 'Prefers stainless steel finish; Kitchen island configuration; Views appliance as statement piece',
                'overall_rating': 4.5,
                'design_rating': 4.8,
                'functionality_rating': 4.2,
                'value_rating': 3.8,
                'positive_sentiment_summary': 'Positive feedback focuses on: beautiful, stunning, great',
                'negative_sentiment_summary': 'Concerns include: expensive',
                'design_trends': 'Panel-ready appliance trend; Smart appliance integration',
                'competitor_comparison': 'Sub Zero; Thermador',
                'price_sentiment': 'Luxury positioning accepted',
                'installation_insights': 'Professional installation required; Plumbing/electrical considerations',
                'raw_review_text': f'Just finished our kitchen renovation with {brand} {appliance_name}. The design is absolutely stunning and it performs beautifully. Installation was smooth with our contractor. Worth every penny for the luxury feel.',
                'search_time': 2.5
            },
            {
                'source': 'Reddit',
                'review_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'reviewer_type': 'Designer/Architect',
                'renovation_context': 'Modern kitchen design; Luxury budget',
                'design_insights': 'Interested in panel-ready/integrated design; Minimalist design preference',
                'overall_rating': 4.2,
                'design_rating': 4.5,
                'functionality_rating': 4.0,
                'value_rating': 3.5,
                'positive_sentiment_summary': 'Positive feedback focuses on: elegant, sleek, modern',
                'negative_sentiment_summary': 'Some negative feedback',
                'design_trends': 'Matte black finish trend; Panel-ready appliance trend',
                'competitor_comparison': 'Gaggenau; Miele',
                'price_sentiment': 'Luxury positioning accepted',
                'installation_insights': 'Professional installation required',
                'raw_review_text': f'As a designer, I love the {brand} {appliance_name} for its clean lines and modern aesthetic. Perfect for contemporary kitchens. The panel-ready option is excellent for seamless integration.',
                'search_time': 2.1
            }
        ]
        return demo_reviews 