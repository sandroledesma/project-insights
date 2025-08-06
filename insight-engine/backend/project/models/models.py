from datetime import datetime
from project import db

class AITool(db.Model):
    """AI Tool model with enhanced insight fields"""
    __tablename__ = 'ai_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    website = db.Column(db.String(500))
    short_description = db.Column(db.Text)
    pricing_model = db.Column(db.String(100))  # e.g., 'Freemium', 'Subscription', 'Pay-per-use'
    primary_use_case = db.Column(db.String(100))  # e.g., 'Content Creation', 'Automation', 'Image Generation'
    
    # New insight fields
    insight_snippet = db.Column(db.Text)  # AI-generated summary of key takeaways
    ideal_for_tags = db.Column(db.String(500))  # Comma-separated tags like 'Solo Founders, Enterprise, Creative Teams'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'short_description': self.short_description,
            'pricing_model': self.pricing_model,
            'primary_use_case': self.primary_use_case,
            'insight_snippet': self.insight_snippet,
            'ideal_for_tags': self.ideal_for_tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class LuxuryAppliance(db.Model):
    """Luxury Appliance model with enhanced insight fields"""
    __tablename__ = 'luxury_appliances'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))  # e.g., 'Refrigerator', 'Oven', 'Dishwasher'
    model_number = db.Column(db.String(100))
    msrp = db.Column(db.Integer)  # Manufacturer's Suggested Retail Price
    price_range = db.Column(db.String(100))  # e.g., '$8,000 - $12,000'
    website = db.Column(db.String(500))
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    design_style = db.Column(db.String(100))
    finish_options = db.Column(db.Text)
    dimensions = db.Column(db.String(200))
    energy_rating = db.Column(db.String(50))
    warranty = db.Column(db.String(100))
    
    # New insight fields
    insight_snippet = db.Column(db.Text)  # e.g., "Praised for its whisper-quiet operation, but owners note the ice maker can be slow."
    style_tags = db.Column(db.String(500))  # e.g., 'Modern, Sleek, Professional-Grade'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'model_number': self.model_number,
            'msrp': self.msrp,
            'price_range': self.price_range,
            'website': self.website,
            'description': self.description,
            'features': self.features,
            'design_style': self.design_style,
            'finish_options': self.finish_options,
            'dimensions': self.dimensions,
            'energy_rating': self.energy_rating,
            'warranty': self.warranty,
            'insight_snippet': self.insight_snippet,
            'style_tags': self.style_tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AggregatedReview(db.Model):
    """Aggregated Review model"""
    __tablename__ = 'aggregated_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Simple foreign key relationships
    ai_tool_id = db.Column(db.Integer, db.ForeignKey('ai_tools.id'), nullable=True)
    luxury_appliance_id = db.Column(db.Integer, db.ForeignKey('luxury_appliances.id'), nullable=True)
    
    # Rating fields
    overall_rating = db.Column(db.Float)
    ease_of_use_score = db.Column(db.Float)
    feature_score = db.Column(db.Float)
    value_for_money_score = db.Column(db.Float)
    
    # Sentiment analysis fields
    positive_sentiment_summary = db.Column(db.Text)
    negative_sentiment_summary = db.Column(db.Text)
    
    # Additional fields for luxury appliances
    design_rating = db.Column(db.Float)
    functionality_rating = db.Column(db.Float)
    value_rating = db.Column(db.Float)
    
    # Insight fields
    key_insights = db.Column(db.Text)  # AI-generated key insights
    common_complaints = db.Column(db.Text)  # Most common complaints
    standout_features = db.Column(db.Text)  # Features that stand out positively
    
    # Metadata
    total_reviews_analyzed = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ai_tool = db.relationship('AITool', backref='reviews')
    luxury_appliance = db.relationship('LuxuryAppliance', backref='reviews')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'ai_tool_id': self.ai_tool_id,
            'luxury_appliance_id': self.luxury_appliance_id,
            'overall_rating': self.overall_rating,
            'ease_of_use_score': self.ease_of_use_score,
            'feature_score': self.feature_score,
            'value_for_money_score': self.value_for_money_score,
            'positive_sentiment_summary': self.positive_sentiment_summary,
            'negative_sentiment_summary': self.negative_sentiment_summary,
            'design_rating': self.design_rating,
            'functionality_rating': self.functionality_rating,
            'value_rating': self.value_rating,
            'key_insights': self.key_insights,
            'common_complaints': self.common_complaints,
            'standout_features': self.standout_features,
            'total_reviews_analyzed': self.total_reviews_analyzed,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 