# Insight Engine Backend

A robust Flask-based API for the Insight Engine review aggregator, providing deep insights for brands and products across all industries.

## Features

- **Multi-Industry API**: Comprehensive endpoints for any product category
- **AI-Powered Insights**: Automated sentiment analysis and trend detection
- **Scalable Architecture**: Blueprint-based modular design
- **Database Migrations**: Flask-Migrate for schema management
- **Real-Time Data**: Integration with multiple review sources

## Project Structure

```
backend/
├── project/
│   ├── __init__.py          # Application factory
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ai_tools.py      # AI tools endpoints
│   │   └── luxury_appliances.py  # Luxury appliances endpoints
│   └── models/
│       ├── __init__.py
│       └── models.py        # SQLAlchemy models
├── config.py                # Configuration management
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   flask init-db
   ```

3. **Seed Sample Data**:
   ```bash
   flask seed-ai-tools
   flask seed-luxury-appliances
   flask seed-reviews
   ```

4. **Run the Server**:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5001`

## API Endpoints

### Health Check
- `GET /health` - Server health status

### AI Tools
- `GET /api/ai-tools` - List all AI tools with insights
- `GET /api/ai-tools/<id>` - Get specific AI tool details
- `GET /api/ai-tools/<id>/reviews` - Get reviews for specific tool
- `GET /api/ai-tools/insights` - Get aggregated insights

### Luxury Appliances
- `GET /api/luxury-appliances` - List all luxury appliances
- `GET /api/luxury-appliances/<id>` - Get specific appliance details
- `GET /api/luxury-appliances/<id>/reviews` - Get reviews for specific appliance
- `GET /api/luxury-appliances/insights` - Get aggregated insights
- `GET /api/luxury-appliances/brands` - Get brand statistics

## Database Models

### AITool
- Core fields: name, website, short_description, pricing_model, primary_use_case
- Insight fields: insight_snippet, ideal_for_tags

### LuxuryAppliance
- Core fields: name, brand, category, model_number, msrp, features
- Insight fields: insight_snippet, style_tags

### AggregatedReview
- Rating fields: overall_rating, ease_of_use_score, feature_score, value_for_money_score
- Insight fields: key_insights, common_complaints, standout_features
- Supports both AI tools and luxury appliances via foreign keys

## Configuration

Environment variables can be set in `.env`:
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API client secret

## Development

- **Debug Mode**: Set `debug=True` in `run.py`
- **Database**: SQLite by default, can be changed to PostgreSQL
- **CORS**: Configured for frontend at `http://localhost:3000`

## CLI Commands

- `flask init-db` - Initialize database tables
- `flask seed-ai-tools` - Seed sample AI tools
- `flask seed-luxury-appliances` - Seed sample luxury appliances
- `flask seed-reviews` - Seed sample aggregated reviews

## Future Expansion

The backend is designed to easily support new product categories:
- Consumer Electronics
- Fashion & Beauty
- Automotive
- Food & Beverage
- Healthcare & Wellness
- And many more...

Each new category can be added by:
1. Creating new models in `project/models/models.py`
2. Adding API blueprints in `project/api/`
3. Creating seed data commands in `run.py` 