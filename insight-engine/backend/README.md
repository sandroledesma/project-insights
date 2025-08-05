# Insight-Engine Backend

Flask-based REST API for the Insight-Engine AI platform review aggregator.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Docker (optional, for database)

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

4. **Start PostgreSQL database:**
   
   **Option A: Using Docker (Recommended)**
   ```bash
   docker run --name insight-engine-db \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=insight_engine \
     -p 5432:5432 \
     -d postgres:13
   ```
   
   **Option B: Local PostgreSQL**
   - Install PostgreSQL on your system
   - Create a database named `insight_engine`
   - Update the `DATABASE_URL` in your `.env` file

5. **Initialize database:**
   ```bash
   flask init-db
   flask seed-db
   ```

6. **Run the development server:**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /api/ai-tools
Returns a list of all AI tools.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "ChatGPT",
      "website": "https://chat.openai.com",
      "short_description": "Advanced language model for conversation and text generation",
      "pricing_model": "Freemium",
      "primary_use_case": "Content Creation"
    }
  ],
  "count": 1
}
```

### GET /api/ai-tools/<id>
Returns details for a specific AI tool including aggregated review data.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "ChatGPT",
    "website": "https://chat.openai.com",
    "short_description": "Advanced language model for conversation and text generation",
    "pricing_model": "Freemium",
    "primary_use_case": "Content Creation",
    "aggregated_review": {
      "id": 1,
      "tool_id": 1,
      "overall_rating": 4.5,
      "ease_of_use_score": 4.2,
      "feature_score": 4.7,
      "value_for_money_score": 4.0,
      "positive_sentiment_summary": "Users love the conversational interface",
      "negative_sentiment_summary": "Some users find the pricing confusing"
    }
  }
}
```

## Database Models

### AITool
Represents an AI platform or tool.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | Tool name (unique) |
| `website` | String | Official website URL |
| `short_description` | Text | Brief description |
| `pricing_model` | String | Pricing model (e.g., "Freemium", "Subscription") |
| `primary_use_case` | String | Main use case (e.g., "Content Creation") |

### AggregatedReview
Represents consolidated review data for an AI tool.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `tool_id` | Integer | Foreign key to AITool |
| `overall_rating` | Float | Overall rating (0.0-5.0) |
| `ease_of_use_score` | Float | Ease of use rating |
| `feature_score` | Float | Feature completeness rating |
| `value_for_money_score` | Float | Value for money rating |
| `positive_sentiment_summary` | Text | Summary of positive feedback |
| `negative_sentiment_summary` | Text | Summary of negative feedback |

## Development

### Adding Sample Data

Use the Flask CLI to add sample data:

```bash
flask seed-db
```

### Database Migrations

For production, consider using Flask-Migrate for database migrations:

```bash
pip install Flask-Migrate
```

### Testing

Run tests (when implemented):

```bash
python -m pytest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/insight_engine` |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `1` |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── ai_tool.py
│   │   └── aggregated_review.py
│   └── routes/              # API routes
│       ├── __init__.py
│       └── ai_tools.py
├── requirements.txt          # Python dependencies
├── run.py                   # Application entry point
└── .env.example            # Environment variables template
``` 