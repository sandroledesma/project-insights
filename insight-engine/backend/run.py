from app import create_app, db
from app.models import AITool, AggregatedReview

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command("seed-db")
def seed_db():
    """Seed the database with sample data"""
    # Create sample AI tools
    tools = [
        AITool(
            name="ChatGPT",
            website="https://chat.openai.com",
            short_description="Advanced language model for conversation and text generation",
            pricing_model="Freemium",
            primary_use_case="Content Creation"
        ),
        AITool(
            name="Midjourney",
            website="https://midjourney.com",
            short_description="AI-powered image generation from text descriptions",
            pricing_model="Subscription",
            primary_use_case="Image Generation"
        ),
        AITool(
            name="Zapier",
            website="https://zapier.com",
            short_description="Automate workflows between different apps and services",
            pricing_model="Pay-per-use",
            primary_use_case="Automation"
        )
    ]
    
    for tool in tools:
        db.session.add(tool)
    
    db.session.commit()
    print("Sample AI tools added to database!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 