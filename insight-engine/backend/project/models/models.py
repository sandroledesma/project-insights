from datetime import datetime
from project import db


class Category(db.Model):
    """Category model - top level categorization (e.g., 'Technology', 'Appliances')"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)  # Brief description of the category
    icon_svg = db.Column(db.Text)  # SVG icon as string
    status = db.Column(db.String(20), default='Live')  # Live, Coming Soon, New
    display_order = db.Column(db.Integer, default=0)  # For ordering in UI
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_subcategories=False):
        """Convert model to dictionary"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_svg': self.icon_svg,
            'status': self.status,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_subcategories:
            result['subcategories'] = [sc.to_dict() for sc in self.subcategories]
            result['total_products'] = sum(len(sc.products) for sc in self.subcategories)
        
        return result


class SubCategory(db.Model):
    """SubCategory model - specific categorization (e.g., 'AI Tools', 'Luxury Appliances')"""
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)  # Brief description of the subcategory
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    status = db.Column(db.String(20), default='Live')  # Live, Coming Soon, New
    display_order = db.Column(db.Integer, default=0)  # For ordering in UI
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='subcategory', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_products_count=True):
        """Convert model to dictionary"""
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.name.lower().replace(' ', '-'),
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'status': self.status,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_products_count:
            result['product_count'] = len(self.products)
        
        return result


class Product(db.Model):
    """Product model - central unified table for all products"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    short_description = db.Column(db.Text)
    insight_snippet = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attributes = db.relationship('ProductAttribute', backref='product', lazy=True, cascade='all, delete-orphan')
    price_history = db.relationship('PriceHistory', backref='product', lazy=True, cascade='all, delete-orphan')
    aggregated_review = db.relationship('AggregatedReview', backref='product', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_details=False):
        """Convert model to dictionary"""
        base_dict = {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'short_description': self.short_description,
            'insight_snippet': self.insight_snippet,
            'image_url': self.image_url,
            'subcategory_id': self.subcategory_id,
            'subcategory_name': self.subcategory.name if self.subcategory else None,
            'category_name': self.subcategory.category.name if self.subcategory and self.subcategory.category else None,
            'overall_rating': self.aggregated_review.overall_rating if self.aggregated_review else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Include detailed information if requested
        if include_details:
            base_dict.update({
                'attributes': [attr.to_dict() for attr in self.attributes],
                'price_history': [price.to_dict() for price in self.price_history],
                'aggregated_review': self.aggregated_review.to_dict() if self.aggregated_review else None
            })
        
        return base_dict


class ProductAttribute(db.Model):
    """ProductAttribute model - flexible key-value specs for products"""
    __tablename__ = 'product_attributes'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)  # e.g., 'Pricing Model', 'Style Tags', 'MSRP'
    value = db.Column(db.Text, nullable=False)       # e.g., 'Freemium', 'Modern, Sleek', '14449'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'product_id': self.product_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PriceHistory(db.Model):
    """PriceHistory model - track price changes over time"""
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    retailer_name = db.Column(db.String(100), nullable=False)
    date_recorded = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'price': self.price,
            'retailer_name': self.retailer_name,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None,
            'product_id': self.product_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AggregatedReview(db.Model):
    """AggregatedReview model - comprehensive review aggregation for products"""
    __tablename__ = 'aggregated_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
    
    # Core rating fields
    overall_rating = db.Column(db.Float)
    ease_of_use_score = db.Column(db.Float)
    feature_score = db.Column(db.Float)
    value_for_money_score = db.Column(db.Float)
    
    # Additional rating fields (useful for appliances and other products)
    design_rating = db.Column(db.Float)
    functionality_rating = db.Column(db.Float)
    reliability_rating = db.Column(db.Float)
    
    # Sentiment analysis fields
    positive_sentiment_summary = db.Column(db.Text)
    negative_sentiment_summary = db.Column(db.Text)
    
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
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'overall_rating': self.overall_rating,
            'ease_of_use_score': self.ease_of_use_score,
            'feature_score': self.feature_score,
            'value_for_money_score': self.value_for_money_score,
            'design_rating': self.design_rating,
            'functionality_rating': self.functionality_rating,
            'reliability_rating': self.reliability_rating,
            'positive_sentiment_summary': self.positive_sentiment_summary,
            'negative_sentiment_summary': self.negative_sentiment_summary,
            'key_insights': self.key_insights,
            'common_complaints': self.common_complaints,
            'standout_features': self.standout_features,
            'total_reviews_analyzed': self.total_reviews_analyzed,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }