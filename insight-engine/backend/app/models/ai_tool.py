from app import db
from sqlalchemy.orm import relationship

class AITool(db.Model):
    """
    AI Tool model representing different AI platforms and tools
    """
    __tablename__ = 'ai_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    website = db.Column(db.String(500))
    short_description = db.Column(db.Text)
    pricing_model = db.Column(db.String(100))  # e.g., 'Freemium', 'Subscription', 'Pay-per-use'
    primary_use_case = db.Column(db.String(100))  # e.g., 'Content Creation', 'Automation', 'Image Generation'
    
    # Relationship to aggregated reviews
    aggregated_reviews = relationship("AggregatedReview", back_populates="tool", cascade="all, delete-orphan")
    
    def to_dict(self):
        """
        Convert model instance to dictionary for JSON serialization
        """
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'short_description': self.short_description,
            'pricing_model': self.pricing_model,
            'primary_use_case': self.primary_use_case
        }
    
    def __repr__(self):
        return f'<AITool {self.name}>' 