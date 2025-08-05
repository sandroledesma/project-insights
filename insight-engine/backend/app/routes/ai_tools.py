from flask import Blueprint, jsonify, request
from app import db
from app.models import AITool, AggregatedReview

ai_tools_bp = Blueprint('ai_tools', __name__)

@ai_tools_bp.route('/ai-tools', methods=['GET'])
def get_ai_tools():
    """
    GET /api/ai-tools
    Returns a JSON list of all AI tools
    """
    try:
        tools = AITool.query.all()
        tools_data = [tool.to_dict() for tool in tools]
        
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