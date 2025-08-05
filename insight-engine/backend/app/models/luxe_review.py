from app import db
from datetime import datetime

class LuxeReview(db.Model):
    """Luxury Appliance Review model for tracking reviews and design insights"""
    __tablename__ = 'luxe_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    appliance_id = db.Column(db.Integer, db.ForeignKey('luxe_appliances.id'), nullable=False)
    source = db.Column(db.String(100))  # e.g., 'Reddit', 'Houzz', 'Architectural Digest'
    review_date = db.Column(db.DateTime)
    reviewer_type = db.Column(db.String(100))  # e.g., 'Homeowner', 'Designer', 'Architect', 'Contractor'
    renovation_context = db.Column(db.Text)  # Kitchen renovation context
    design_insights = db.Column(db.Text)  # Design-related insights
    overall_rating = db.Column(db.Float)  # 1-5 scale
    design_rating = db.Column(db.Float)  # Design/aesthetic rating
    functionality_rating = db.Column(db.Float)  # Performance rating
    value_rating = db.Column(db.Float)  # Value for money rating
    positive_sentiment_summary = db.Column(db.Text)
    negative_sentiment_summary = db.Column(db.Text)
    design_trends = db.Column(db.Text)  # Design trends mentioned
    competitor_comparison = db.Column(db.Text)  # Mentions of other brands
    price_sentiment = db.Column(db.Text)  # Price-related feedback
    installation_insights = db.Column(db.Text)  # Installation feedback
    raw_review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'appliance_id': self.appliance_id,
            'source': self.source,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'reviewer_type': self.reviewer_type,
            'renovation_context': self.renovation_context,
            'design_insights': self.design_insights,
            'overall_rating': self.overall_rating,
            'design_rating': self.design_rating,
            'functionality_rating': self.functionality_rating,
            'value_rating': self.value_rating,
            'positive_sentiment_summary': self.positive_sentiment_summary,
            'negative_sentiment_summary': self.negative_sentiment_summary,
            'design_trends': self.design_trends,
            'competitor_comparison': self.competitor_comparison,
            'price_sentiment': self.price_sentiment,
            'installation_insights': self.installation_insights,
            'raw_review_text': self.raw_review_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 