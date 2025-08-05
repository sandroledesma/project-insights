from flask import Blueprint, jsonify, request
from app.models.luxe_appliance import LuxeAppliance
from app.models.luxe_review import LuxeReview
from app import db
import logging

logger = logging.getLogger(__name__)

luxe_appliances_bp = Blueprint('luxe_appliances', __name__)

@luxe_appliances_bp.route('/luxe-appliances', methods=['GET'])
def get_luxe_appliances():
    """
    GET /api/luxe-appliances
    Returns a JSON list of all luxury appliances with their aggregated review data
    """
    try:
        appliances = LuxeAppliance.query.all()
        appliances_data = []
        
        for appliance in appliances:
            appliance_dict = appliance.to_dict()
            
            # Get aggregated review data
            reviews = LuxeReview.query.filter_by(appliance_id=appliance.id).all()
            
            if reviews:
                # Calculate aggregated metrics
                total_reviews = len(reviews)
                avg_overall = sum(r.overall_rating for r in reviews if r.overall_rating) / len([r for r in reviews if r.overall_rating]) if [r for r in reviews if r.overall_rating] else 0
                avg_design = sum(r.design_rating for r in reviews if r.design_rating) / len([r for r in reviews if r.design_rating]) if [r for r in reviews if r.design_rating] else 0
                avg_functionality = sum(r.functionality_rating for r in reviews if r.functionality_rating) / len([r for r in reviews if r.functionality_rating]) if [r for r in reviews if r.functionality_rating] else 0
                avg_value = sum(r.value_rating for r in reviews if r.value_rating) / len([r for r in reviews if r.value_rating]) if [r for r in reviews if r.value_rating] else 0
                
                # Get recent reviews
                recent_reviews = sorted(reviews, key=lambda x: x.created_at, reverse=True)[:3]
                
                appliance_dict['aggregated_review'] = {
                    'total_reviews': total_reviews,
                    'overall_rating': round(avg_overall, 1) if avg_overall else None,
                    'design_rating': round(avg_design, 1) if avg_design else None,
                    'functionality_rating': round(avg_functionality, 1) if avg_functionality else None,
                    'value_rating': round(avg_value, 1) if avg_value else None,
                    'recent_reviews': [r.to_dict() for r in recent_reviews]
                }
            else:
                appliance_dict['aggregated_review'] = None
            
            appliances_data.append(appliance_dict)
        
        return jsonify({
            'success': True,
            'data': appliances_data,
            'count': len(appliances_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching luxury appliances: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxe_appliances_bp.route('/luxe-appliances/<int:appliance_id>', methods=['GET'])
def get_luxe_appliance(appliance_id):
    """
    GET /api/luxe-appliances/<id>
    Returns details for a single luxury appliance with all reviews
    """
    try:
        appliance = LuxeAppliance.query.get_or_404(appliance_id)
        appliance_data = appliance.to_dict()
        
        # Get all reviews for this appliance
        reviews = LuxeReview.query.filter_by(appliance_id=appliance_id).order_by(LuxeReview.created_at.desc()).all()
        appliance_data['reviews'] = [review.to_dict() for review in reviews]
        
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

@luxe_appliances_bp.route('/luxe-appliances/<int:appliance_id>/reviews', methods=['GET'])
def get_luxe_reviews(appliance_id):
    """
    GET /api/luxe-appliances/<id>/reviews
    Returns reviews for a specific luxury appliance
    """
    try:
        appliance = LuxeAppliance.query.get_or_404(appliance_id)
        reviews = LuxeReview.query.filter_by(appliance_id=appliance_id).order_by(LuxeReview.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': {
                'appliance': appliance.to_dict(),
                'reviews': [review.to_dict() for review in reviews],
                'count': len(reviews)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching reviews for appliance {appliance_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxe_appliances_bp.route('/luxe-appliances/<int:appliance_id>/refresh-reviews', methods=['POST'])
def refresh_luxe_reviews(appliance_id):
    """
    POST /api/luxe-appliances/<id>/refresh-reviews
    Manually trigger review refresh for a luxury appliance
    """
    try:
        appliance = LuxeAppliance.query.get_or_404(appliance_id)
        
        # Temporarily return demo data instead of calling Reddit service
        return jsonify({
            'success': True,
            'message': f'Reviews refresh temporarily disabled for {appliance.name}',
            'total_reviews': 0,
            'saved_count': 0,
            'search_time': 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error refreshing reviews for appliance {appliance_id}: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@luxe_appliances_bp.route('/luxe-appliances/design-insights', methods=['GET'])
def get_design_insights():
    """
    GET /api/luxe-appliances/design-insights
    Returns aggregated design insights across all luxury appliances
    """
    try:
        # Get all reviews
        reviews = LuxeReview.query.all()
        
        # Extract design insights (simplified to avoid hanging)
        design_trends = {}
        competitor_mentions = {}
        price_insights = {}
        installation_insights = {}
        
        for review in reviews:
            if review.design_trends:
                for trend in review.design_trends.split(';'):
                    trend = trend.strip()
                    if trend:
                        design_trends[trend] = design_trends.get(trend, 0) + 1
            
            if review.competitor_comparison:
                for competitor in review.competitor_comparison.split(';'):
                    competitor = competitor.strip()
                    if competitor:
                        competitor_mentions[competitor] = competitor_mentions.get(competitor, 0) + 1
            
            if review.price_sentiment:
                price_insights[review.price_sentiment] = price_insights.get(review.price_sentiment, 0) + 1
            
            if review.installation_insights:
                for insight in review.installation_insights.split(';'):
                    insight = insight.strip()
                    if insight:
                        installation_insights[insight] = installation_insights.get(insight, 0) + 1
        
        return jsonify({
            'success': True,
            'data': {
                'design_trends': design_trends,
                'competitor_mentions': competitor_mentions,
                'price_insights': price_insights,
                'installation_insights': installation_insights,
                'total_reviews': len(reviews)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching design insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 