from app import db
from datetime import datetime

class LuxeAppliance(db.Model):
    """Luxury Appliance model for tracking high-end appliance brands and models"""
    __tablename__ = 'luxe_appliances'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))  # e.g., 'Refrigerator', 'Range', 'Dishwasher', 'Oven'
    model_number = db.Column(db.String(100))
    price_range = db.Column(db.String(50))  # e.g., '$5,000-$8,000', '$10,000+'
    website = db.Column(db.String(500))
    description = db.Column(db.Text)
    features = db.Column(db.Text)  # Key features and specifications
    design_style = db.Column(db.String(100))  # e.g., 'Modern', 'Traditional', 'Transitional'
    finish_options = db.Column(db.Text)  # Available finishes
    dimensions = db.Column(db.String(200))
    energy_rating = db.Column(db.String(50))
    warranty = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'model_number': self.model_number,
            'price_range': self.price_range,
            'website': self.website,
            'description': self.description,
            'features': self.features,
            'design_style': self.design_style,
            'finish_options': self.finish_options,
            'dimensions': self.dimensions,
            'energy_rating': self.energy_rating,
            'warranty': self.warranty,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 