from app import create_app, db
from app.models.luxe_appliance import LuxeAppliance
from app.models.luxe_review import LuxeReview
from app.services.luxe_service import LuxeService

app = create_app()

with app.app_context():
    try:
        print("Testing route logic...")
        
        # Test the exact logic from the route
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
                    'recent_reviews': [r.to_dict() for r in recent_reviews],
                    'design_trends': {},
                    'competitor_mentions': {},
                    'price_insights': {},
                    'installation_insights': {}
                }
            else:
                appliance_dict['aggregated_review'] = None
            
            appliances_data.append(appliance_dict)
        
        print(f"Processed {len(appliances_data)} appliances")
        print("Route logic successful!")
        
    except Exception as e:
        print(f"Route error: {e}")
        import traceback
        traceback.print_exc() 