from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.orm import joinedload
from project.models import AITool, AggregatedReview
from project import db
import logging

logger = logging.getLogger(__name__)

# Create blueprint
ai_tools_bp = Blueprint('ai_tools', __name__)

@ai_tools_bp.route('/ai-tools', methods=['GET'])
def get_ai_tools():
    """
    GET /api/ai-tools
    Returns all AI tools with insights and aggregated review data
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', current_app.config['ITEMS_PER_PAGE'], type=int)
        search = request.args.get('search', '').strip()
        use_case = request.args.get('use_case', '').strip()
        pricing_model = request.args.get('pricing_model', '').strip()
        
        # Build query
        query = AITool.query
        
        # Apply filters
        if search:
            query = query.filter(
                AITool.name.ilike(f'%{search}%') |
                AITool.short_description.ilike(f'%{search}%') |
                AITool.insight_snippet.ilike(f'%{search}%')
            )
        
        if use_case:
            query = query.filter(AITool.primary_use_case.ilike(f'%{use_case}%'))
        
        if pricing_model:
            query = query.filter(AITool.pricing_model.ilike(f'%{pricing_model}%'))
        
        # Paginate results
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dictionary with review data
        tools_data = []
        for tool in pagination.items:
            tool_data = tool.to_dict()
            
            # Get aggregated review data - fixed to handle list properly
            reviews = tool.reviews
            if reviews and len(reviews) > 0:
                aggregated_review = reviews[0]  # Get first review
                tool_data['aggregated_review'] = aggregated_review.to_dict()
                tool_data['overall_rating'] = aggregated_review.overall_rating
            else:
                tool_data['aggregated_review'] = None
                tool_data['overall_rating'] = None
            
            tools_data.append(tool_data)
        
        return jsonify({
            'success': True,
            'data': tools_data,
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
                'use_case': use_case,
                'pricing_model': pricing_model
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching AI tools: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/<int:tool_id>', methods=['GET'])
def get_ai_tool(tool_id):
    """
    GET /api/ai-tools/<id>
    Returns full details for one AI tool with complete review data
    """
    try:
        tool = AITool.query.get_or_404(tool_id)
        
        # Get full data with reviews
        tool_data = tool.to_dict()
        
        # Get aggregated review - fixed to handle list properly
        reviews = tool.reviews
        if reviews and len(reviews) > 0:
            aggregated_review = reviews[0]  # Get first review
            tool_data['aggregated_review'] = aggregated_review.to_dict()
            tool_data['insights'] = {
                'key_insights': aggregated_review.key_insights,
                'common_complaints': aggregated_review.common_complaints,
                'standout_features': aggregated_review.standout_features,
                'total_reviews_analyzed': aggregated_review.total_reviews_analyzed
            }
        else:
            tool_data['aggregated_review'] = None
            tool_data['insights'] = None
        
        return jsonify({
            'success': True,
            'data': tool_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching AI tool {tool_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/<int:tool_id>/reviews', methods=['GET'])
def get_ai_tool_reviews(tool_id):
    """
    GET /api/ai-tools/<id>/reviews
    Returns detailed review data for a specific AI tool
    """
    try:
        tool = AITool.query.get_or_404(tool_id)
        
        # Get aggregated review - fixed to handle list properly
        reviews = tool.reviews
        if reviews and len(reviews) > 0:
            aggregated_review = reviews[0]  # Get first review
            review_data = aggregated_review.to_dict()
        else:
            review_data = None
        
        return jsonify({
            'success': True,
            'data': {
                'tool': tool.to_dict(),
                'review': review_data
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching reviews for AI tool {tool_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_tools_bp.route('/ai-tools/insights', methods=['GET'])
def get_ai_tools_insights():
    """
    GET /api/ai-tools/insights
    Returns aggregated insights across all AI tools
    """
    try:
        # Get all tools with reviews
        tools = AITool.query.all()
        
        insights = {
            'total_tools': len(tools),
            'tools_with_reviews': 0,
            'average_rating': 0,
            'top_use_cases': {},
            'pricing_breakdown': {},
            'common_insights': []
        }
        
        total_rating = 0
        rated_tools = 0
        
        for tool in tools:
            reviews = tool.reviews
            if reviews and len(reviews) > 0:
                review = reviews[0]  # Get first review
                if review.overall_rating:
                    insights['tools_with_reviews'] += 1
                    total_rating += review.overall_rating
                    rated_tools += 1
            
            # Count use cases
            if tool.primary_use_case:
                insights['top_use_cases'][tool.primary_use_case] = \
                    insights['top_use_cases'].get(tool.primary_use_case, 0) + 1
            
            # Count pricing models
            if tool.pricing_model:
                insights['pricing_breakdown'][tool.pricing_model] = \
                    insights['pricing_breakdown'].get(tool.pricing_model, 0) + 1
            
            # Collect insight snippets
            if tool.insight_snippet:
                insights['common_insights'].append(tool.insight_snippet)
        
        if rated_tools > 0:
            insights['average_rating'] = round(total_rating / rated_tools, 2)
        
        return jsonify({
            'success': True,
            'data': insights
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching AI tools insights: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 