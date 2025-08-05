from app import db
from sqlalchemy.orm import relationship

class AggregatedReview(db.Model):
    """
    Aggregated Review model representing consolidated review data for AI tools
    """
    __tablename__ = 'aggregated_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id'), nullable=False)
    overall_rating = db.Column(db.Float, nullable=False)  # 0.0 to 5.0
    ease_of_use_score = db.Column(db.Float)
    feature_score = db.Column(db.Float)
    value_for_money_score = db.Column(db.Float)
    positive_sentiment_summary = db.Column(db.Text)
    negative_sentiment_summary = db.Column(db.Text)
    
    # Relationship to AI tool
    tool = relationship("AITool", back_populates="aggregated_reviews")
    
    def to_dict(self):
        """
        Convert model instance to dictionary for JSON serialization
        """
        return {
            'id': self.id,
            'tool_id': self.tool_id,
            'overall_rating': self.overall_rating,
            'ease_of_use_score': self.ease_of_use_score,
            'feature_score': self.feature_score,
            'value_for_money_score': self.value_for_money_score,
            'positive_sentiment_summary': self.positive_sentiment_summary,
            'negative_sentiment_summary': self.negative_sentiment_summary
        }
    
    def __repr__(self):
        return f'<AggregatedReview {self.tool_id}: {self.overall_rating}>' 