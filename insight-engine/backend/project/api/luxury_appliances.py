from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.orm import joinedload
from project.models import LuxuryAppliance, AggregatedReview
from project import db
import logging

logger = logging.getLogger(__name__)

# Create blueprint
luxury_appliances_bp = Blueprint('luxury_appliances', __name__)

@luxury_appliances_bp.route('/luxury-appliances', methods=['GET'])
def get_luxury_appliances():
    """
    GET /api/luxury-appliances
    Returns all luxury appliances with insights and aggregated review data
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', current_app.config['ITEMS_PER_PAGE'], type=int)
        search = request.args.get('search', '').strip()
        brand = request.args.get('brand', '').strip()
        category = request.args.get('category', '').strip()
        design_style = request.args.get('design_style', '').strip()
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        
        # Build query
        query = LuxuryAppliance.query
        
        # Apply filters
        if search:
            query = query.filter(
                LuxuryAppliance.name.ilike(f'%{search}%') |
                LuxuryAppliance.description.ilike(f'%{search}%') |
                LuxuryAppliance.insight_snippet.ilike(f'%{search}%')
            )
        
        if brand:
            query = query.filter(LuxuryAppliance.brand.ilike(f'%{brand}%'))
        
        if category:
            query = query.filter(LuxuryAppliance.category.ilike(f'%{category}%'))
        
        if design_style:
            query = query.filter(LuxuryAppliance.design_style.ilike(f'%{design_style}%'))
        
        if min_price is not None:
            query = query.filter(LuxuryAppliance.msrp >= min_price)
        
        if max_price is not None:
            query = query.filter(LuxuryAppliance.msrp <= max_price)
        
        # Paginate results
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dictionary with review data
        appliances_data = []
        for appliance in pagination.items:
            appliance_data = appliance.to_dict()
            
            # Get aggregated review data - fixed to handle list properly
            reviews = appliance.reviews
            if reviews and len(reviews) > 0:
                aggregated_review = reviews[0]  # Get first review
                appliance_data['aggregated_review'] = aggregated_review.to_dict()
                appliance_data['overall_rating'] = aggregated_review.overall_rating
            else:
                appliance_data['aggregated_review'] = None
                appliance_data['overall_rating'] = None
            
            appliances_data.append(appliance_data)
        
        return jsonify({
            'success': True,
            'data': appliances_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'filters': {
                'search': search,
                'brand': brand,
                'category': category,
                'design_style': design_style,
                'min_price': min_price,
                'max_price': max_price
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching luxury appliances: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxury_appliances_bp.route('/luxury-appliances/<int:appliance_id>', methods=['GET'])
def get_luxury_appliance(appliance_id):
    """
    GET /api/luxury-appliances/<id>
    Returns full details for one luxury appliance with complete review data
    """
    try:
        appliance = LuxuryAppliance.query.get_or_404(appliance_id)
        
        # Get full data with reviews
        appliance_data = appliance.to_dict()
        
        # Get aggregated review - fixed to handle list properly
        reviews = appliance.reviews
        if reviews and len(reviews) > 0:
            aggregated_review = reviews[0]  # Get first review
            appliance_data['aggregated_review'] = aggregated_review.to_dict()
            appliance_data['insights'] = {
                'key_insights': aggregated_review.key_insights,
                'common_complaints': aggregated_review.common_complaints,
                'standout_features': aggregated_review.standout_features,
                'total_reviews_analyzed': aggregated_review.total_reviews_analyzed
            }
        else:
            appliance_data['aggregated_review'] = None
            appliance_data['insights'] = None
        
        return jsonify({
            'success': True,
            'data': appliance_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching luxury appliance {appliance_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxury_appliances_bp.route('/luxury-appliances/<int:appliance_id>/reviews', methods=['GET'])
def get_luxury_appliance_reviews(appliance_id):
    """
    GET /api/luxury-appliances/<id>/reviews
    Returns detailed review data for a specific luxury appliance
    """
    try:
        appliance = LuxuryAppliance.query.get_or_404(appliance_id)
        
        # Get aggregated review - fixed to handle list properly
        reviews = appliance.reviews
        if reviews and len(reviews) > 0:
            aggregated_review = reviews[0]  # Get first review
            review_data = aggregated_review.to_dict()
        else:
            review_data = None
        
        return jsonify({
            'success': True,
            'data': {
                'appliance': appliance.to_dict(),
                'review': review_data
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching reviews for luxury appliance {appliance_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxury_appliances_bp.route('/luxury-appliances/insights', methods=['GET'])
def get_luxury_appliances_insights():
    """
    GET /api/luxury-appliances/insights
    Returns aggregated insights across all luxury appliances
    """
    try:
        # Get all appliances with reviews
        appliances = LuxuryAppliance.query.all()
        
        insights = {
            'total_appliances': len(appliances),
            'appliances_with_reviews': 0,
            'average_rating': 0,
            'brand_breakdown': {},
            'category_breakdown': {},
            'design_style_breakdown': {},
            'price_range_analysis': {
                'average_msrp': 0,
                'price_ranges': {}
            },
            'common_insights': []
        }
        
        total_rating = 0
        rated_appliances = 0
        total_msrp = 0
        priced_appliances = 0
        
        for appliance in appliances:
            reviews = appliance.reviews
            if reviews and len(reviews) > 0:
                review = reviews[0]  # Get first review
                if review.overall_rating:
                    insights['appliances_with_reviews'] += 1
                    total_rating += review.overall_rating
                    rated_appliances += 1
            
            # Count brands
            if appliance.brand:
                insights['brand_breakdown'][appliance.brand] = \
                    insights['brand_breakdown'].get(appliance.brand, 0) + 1
            
            # Count categories
            if appliance.category:
                insights['category_breakdown'][appliance.category] = \
                    insights['category_breakdown'].get(appliance.category, 0) + 1
            
            # Count design styles
            if appliance.design_style:
                insights['design_style_breakdown'][appliance.design_style] = \
                    insights['design_style_breakdown'].get(appliance.design_style, 0) + 1
            
            # Price analysis
            if appliance.msrp:
                total_msrp += appliance.msrp
                priced_appliances += 1
                
                # Categorize price ranges
                if appliance.msrp < 5000:
                    price_range = 'Under $5,000'
                elif appliance.msrp < 10000:
                    price_range = '$5,000 - $10,000'
                elif appliance.msrp < 15000:
                    price_range = '$10,000 - $15,000'
                else:
                    price_range = 'Over $15,000'
                
                insights['price_range_analysis']['price_ranges'][price_range] = \
                    insights['price_range_analysis']['price_ranges'].get(price_range, 0) + 1
            
            # Collect insight snippets
            if appliance.insight_snippet:
                insights['common_insights'].append(appliance.insight_snippet)
        
        if rated_appliances > 0:
            insights['average_rating'] = round(total_rating / rated_appliances, 2)
        
        if priced_appliances > 0:
            insights['price_range_analysis']['average_msrp'] = round(total_msrp / priced_appliances, 2)
        
        return jsonify({
            'success': True,
            'data': insights
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching luxury appliances insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxury_appliances_bp.route('/luxury-appliances/brands', methods=['GET'])
def get_luxury_appliance_brands():
    """
    GET /api/luxury-appliances/brands
    Returns list of all brands with their appliance counts
    """
    try:
        from sqlalchemy import func
        
        # Get brand statistics - fixed to work with our simplified model
        brand_stats = db.session.query(
            LuxuryAppliance.brand,
            func.count(LuxuryAppliance.id).label('count'),
            func.avg(AggregatedReview.overall_rating).label('avg_rating')
        ).outerjoin(AggregatedReview, LuxuryAppliance.id == AggregatedReview.luxury_appliance_id)\
         .group_by(LuxuryAppliance.brand)\
         .all()
        
        brands_data = []
        for brand, count, avg_rating in brand_stats:
            brands_data.append({
                'brand': brand,
                'appliance_count': count,
                'average_rating': round(avg_rating, 2) if avg_rating else None
            })
        
        return jsonify({
            'success': True,
            'data': brands_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching luxury appliance brands: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 