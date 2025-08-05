from flask import Blueprint, jsonify, request
from app import db
from app.models import AITool, AggregatedReview
import logging
import time

ai_tools_bp = Blueprint('ai_tools', __name__)
# Lazy load RedditService to avoid hanging during startup
_reddit_service = None

def get_reddit_service():
    global _reddit_service
    if _reddit_service is None:
        from app.services.reddit_service import RedditService
        _reddit_service = RedditService()
    return _reddit_service

@ai_tools_bp.route('/ai-tools', methods=['GET'])
def get_ai_tools():
    """
    GET /api/ai-tools
    Returns a JSON list of all AI tools with their aggregated review data
    """
    try:
        tools = AITool.query.all()
        tools_data = []
        
        for tool in tools:
            tool_dict = tool.to_dict()
            
            # Get aggregated review data for this tool
            aggregated_review = AggregatedReview.query.filter_by(tool_id=tool.id).first()
            if aggregated_review:
                tool_dict['aggregated_review'] = aggregated_review.to_dict()
            else:
                tool_dict['aggregated_review'] = None
            
            tools_data.append(tool_dict)
        
        return jsonify({
            'success': True,
            'data': tools_data,
            'count': len(tools_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/<int:tool_id>', methods=['GET'])
def get_ai_tool(tool_id):
    """
    GET /api/ai-tools/<id>
    Returns the details for a single AI tool, including its aggregated review data
    """
    try:
        tool = AITool.query.get_or_404(tool_id)
        
        # Get aggregated review data for this tool
        aggregated_review = AggregatedReview.query.filter_by(tool_id=tool_id).first()
        
        tool_data = tool.to_dict()
        if aggregated_review:
            tool_data['aggregated_review'] = aggregated_review.to_dict()
        else:
            tool_data['aggregated_review'] = None
        
        return jsonify({
            'success': True,
            'data': tool_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/<int:tool_id>/reddit-reviews', methods=['GET'])
def get_reddit_reviews(tool_id):
    """
    GET /api/ai-tools/<id>/reddit-reviews
    Fetch and analyze Reddit reviews for a specific AI tool
    """
    try:
        tool = AITool.query.get_or_404(tool_id)
        
        # Set a timeout for the Reddit search
        start_time = time.time()
        timeout_seconds = 30  # 30 second timeout
        
        # Fetch Reddit reviews
        reddit_service = get_reddit_service()
        reviews = reddit_service.search_reviews(tool.name)
        
        # Check timeout
        if time.time() - start_time > timeout_seconds:
            return jsonify({
                'success': False,
                'error': 'Request timed out. Reddit search took too long.'
            }), 408
        
        # Aggregate the reviews
        aggregated_data = reddit_service.aggregate_reviews(reviews)
        
        # Update or create aggregated review in database
        existing_review = AggregatedReview.query.filter_by(tool_id=tool_id).first()
        
        if existing_review and aggregated_data:
            # Update existing review
            existing_review.overall_rating = aggregated_data['overall_rating']
            existing_review.ease_of_use_score = aggregated_data['ease_of_use_score']
            existing_review.feature_score = aggregated_data['feature_score']
            existing_review.value_for_money_score = aggregated_data['value_for_money_score']
            existing_review.positive_sentiment_summary = aggregated_data['positive_sentiment_summary']
            existing_review.negative_sentiment_summary = aggregated_data['negative_sentiment_summary']
        elif aggregated_data:
            # Create new review
            new_review = AggregatedReview(
                tool_id=tool_id,
                overall_rating=aggregated_data['overall_rating'],
                ease_of_use_score=aggregated_data['ease_of_use_score'],
                feature_score=aggregated_data['feature_score'],
                value_for_money_score=aggregated_data['value_for_money_score'],
                positive_sentiment_summary=aggregated_data['positive_sentiment_summary'],
                negative_sentiment_summary=aggregated_data['negative_sentiment_summary']
            )
            db.session.add(new_review)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'tool': tool.to_dict(),
                'reviews': reviews,
                'aggregated_data': aggregated_data,
                'total_reviews_found': len(reviews),
                'search_time': round(time.time() - start_time, 2)
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching Reddit reviews: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/<int:tool_id>/refresh-reviews', methods=['POST'])
def refresh_reviews(tool_id):
    """
    POST /api/ai-tools/<id>/refresh-reviews
    Manually refresh Reddit reviews for a tool
    """
    try:
        tool = AITool.query.get_or_404(tool_id)
        
        # Set a timeout for the Reddit search
        start_time = time.time()
        timeout_seconds = 30  # 30 second timeout
        
        # Fetch fresh Reddit reviews
        reddit_service = get_reddit_service()
        reviews = reddit_service.search_reviews(tool.name)
        
        # Check timeout
        if time.time() - start_time > timeout_seconds:
            return jsonify({
                'success': False,
                'error': 'Request timed out. Reddit search took too long.'
            }), 408
        
        aggregated_data = reddit_service.aggregate_reviews(reviews)
        
        # Update database
        existing_review = AggregatedReview.query.filter_by(tool_id=tool_id).first()
        
        if existing_review and aggregated_data:
            existing_review.overall_rating = aggregated_data['overall_rating']
            existing_review.ease_of_use_score = aggregated_data['ease_of_use_score']
            existing_review.feature_score = aggregated_data['feature_score']
            existing_review.value_for_money_score = aggregated_data['value_for_money_score']
            existing_review.positive_sentiment_summary = aggregated_data['positive_sentiment_summary']
            existing_review.negative_sentiment_summary = aggregated_data['negative_sentiment_summary']
        elif aggregated_data:
            new_review = AggregatedReview(
                tool_id=tool_id,
                overall_rating=aggregated_data['overall_rating'],
                ease_of_use_score=aggregated_data['ease_of_use_score'],
                feature_score=aggregated_data['feature_score'],
                value_for_money_score=aggregated_data['value_for_money_score'],
                positive_sentiment_summary=aggregated_data['positive_sentiment_summary'],
                negative_sentiment_summary=aggregated_data['negative_sentiment_summary']
            )
            db.session.add(new_review)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Reviews refreshed for {tool.name}',
            'total_reviews': len(reviews),
            'search_time': round(time.time() - start_time, 2)
        }), 200
        
    except Exception as e:
        logging.error(f"Error refreshing reviews: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 