from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import desc
from project import db
from project.models.models import Product, SubCategory, Category, AggregatedReview

# Create the products blueprint
products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products or filter by subcategory
    
    Query Parameters:
    - subcategory: Filter by subcategory name (e.g., 'ai-tools', 'luxury-appliances')
    - page: Page number for pagination (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    
    Returns:
    - JSON response with products list, pagination info, and metadata
    """
    try:
        # Get query parameters
        subcategory_param = request.args.get('subcategory')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Start with base query, joining necessary tables for sorting
        query = db.session.query(Product).outerjoin(AggregatedReview)
        
        # Filter by subcategory if provided
        if subcategory_param:
            # Convert kebab-case to proper case for lookup
            subcategory_name = subcategory_param.replace('-', ' ').title()
            if subcategory_name.lower() == 'ai tools':
                subcategory_name = 'AI Tools'
            
            query = query.join(SubCategory).filter(SubCategory.name == subcategory_name)
        
        # Sort by overall_rating (highest first), then by name
        # Note: SQLite doesn't support NULLS LAST, so we use a different approach
        query = query.order_by(
            desc(AggregatedReview.overall_rating.is_(None)),
            desc(AggregatedReview.overall_rating),
            Product.name
        )
        
        # Paginate results
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Convert products to dictionary format
        products = []
        for product in pagination.items:
            product_dict = product.to_dict(include_details=False)
            products.append(product_dict)
        
        # Prepare response
        response = {
            'products': products,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next,
                'prev_num': pagination.prev_num,
                'next_num': pagination.next_num
            },
            'filters': {
                'subcategory': subcategory_param
            },
            'total_count': pagination.total
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching products: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to fetch products'
        }), 500


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get detailed information for a single product
    
    Parameters:
    - product_id: Integer ID of the product
    
    Returns:
    - JSON response with full product details including attributes, price history, and reviews
    """
    try:
        # Fetch product with all related data
        product = db.session.query(Product).filter_by(id=product_id).first()
        
        if not product:
            return jsonify({
                'error': 'Product not found',
                'message': f'No product found with ID {product_id}'
            }), 404
        
        # Convert to dictionary with full details
        product_data = product.to_dict(include_details=True)
        
        return jsonify({
            'product': product_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching product {product_id}: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': f'Failed to fetch product with ID {product_id}'
        }), 500


@products_bp.route('/products/subcategories', methods=['GET'])
def get_subcategories():
    """
    Get all available subcategories with their categories
    
    Returns:
    - JSON response with list of subcategories and their parent categories
    """
    try:
        subcategories = db.session.query(SubCategory).join(Category).all()
        
        subcategories_data = []
        for subcategory in subcategories:
            subcategories_data.append({
                'id': subcategory.id,
                'name': subcategory.name,
                'slug': subcategory.name.lower().replace(' ', '-'),
                'category': {
                    'id': subcategory.category.id,
                    'name': subcategory.category.name
                },
                'product_count': len(subcategory.products)
            })
        
        return jsonify({
            'subcategories': subcategories_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching subcategories: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to fetch subcategories'
        }), 500


@products_bp.route('/products/categories', methods=['GET'])
def get_categories():
    """
    Get all available categories with their subcategories
    
    Returns:
    - JSON response with list of categories and their subcategories
    """
    try:
        categories = db.session.query(Category).order_by(Category.display_order, Category.name).all()
        
        categories_data = []
        for category in categories:
            # Get subcategories ordered by display_order
            subcategories_data = []
            ordered_subcategories = sorted(category.subcategories, key=lambda x: (x.display_order, x.name))
            
            for subcategory in ordered_subcategories:
                subcategories_data.append(subcategory.to_dict(include_products_count=True))
            
            category_dict = category.to_dict(include_subcategories=False)
            category_dict['subcategories'] = subcategories_data
            category_dict['total_products'] = sum(len(sc.products) for sc in category.subcategories)
            
            categories_data.append(category_dict)
        
        return jsonify({
            'categories': categories_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching categories: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to fetch categories'
        }), 500


# Error handlers for the blueprint
@products_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404


@products_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'error': 'Bad request',
        'message': 'The request was invalid'
    }), 400


@products_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500