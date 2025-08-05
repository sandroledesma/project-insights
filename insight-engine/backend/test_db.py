from app import create_app, db
from app.models.luxe_appliance import LuxeAppliance

app = create_app()

with app.app_context():
    try:
        print("Testing database connection...")
        appliances = LuxeAppliance.query.all()
        print(f"Found {len(appliances)} appliances")
        for appliance in appliances[:3]:
            print(f"- {appliance.name} ({appliance.brand})")
        print("Database query successful!")
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc() 