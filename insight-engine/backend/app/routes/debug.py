from flask import Blueprint, jsonify
import time

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/debug/simple', methods=['GET'])
def simple_test():
    """Simple test without any database operations"""
    return jsonify({'message': 'Simple test works!', 'timestamp': time.time()})

@debug_bp.route('/debug/db-test', methods=['GET'])
def db_test():
    """Test with database import but no query"""
    try:
        from app import db
        from app.models.luxe_appliance import LuxeAppliance
        return jsonify({'message': 'DB import works!', 'timestamp': time.time()})
    except Exception as e:
        return jsonify({'error': str(e), 'timestamp': time.time()}), 500

@debug_bp.route('/debug/db-query', methods=['GET'])
def db_query_test():
    """Test with actual database query"""
    try:
        from app import db
        from app.models.luxe_appliance import LuxeAppliance
        
        # Simple count query
        count = LuxeAppliance.query.count()
        return jsonify({'message': 'DB query works!', 'count': count, 'timestamp': time.time()})
    except Exception as e:
        return jsonify({'error': str(e), 'timestamp': time.time()}), 500 