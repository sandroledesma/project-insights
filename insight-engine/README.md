# Insight-Engine

A comprehensive review aggregator for AI platforms and tools, helping users discover and compare the best AI solutions.

## Project Structure

```
insight-engine/
├── backend/          # Flask API server
│   ├── app/         # Application code
│   ├── requirements.txt
│   └── run.py
└── frontend/        # React frontend
    ├── src/
    ├── public/
    └── package.json
```

## Features

- **AI Tools Directory**: Browse and search through AI platforms
- **Review Aggregation**: Consolidated ratings and sentiment analysis
- **Advanced Filtering**: Filter by use case, pricing model, and ratings
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **RESTful API**: Clean, documented backend API

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database (using Docker):
   ```bash
   docker run --name insight-engine-db \
     -e POSTGRES_PASSWORD=password \
     -e POSTGRES_DB=insight_engine \
     -p 5432:5432 \
     -d postgres:13
   ```

5. Initialize the database:
   ```bash
   flask init-db
   flask seed-db
   ```

6. Run the backend server:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /api/ai-tools` - Get all AI tools
- `GET /api/ai-tools/<id>` - Get specific AI tool with aggregated reviews

## Database Models

### AITool
- `id` (Primary Key)
- `name` (String, unique)
- `website` (String)
- `short_description` (Text)
- `pricing_model` (String)
- `primary_use_case` (String)

### AggregatedReview
- `id` (Primary Key)
- `tool_id` (Foreign Key to AITool)
- `overall_rating` (Float, 0.0-5.0)
- `ease_of_use_score` (Float)
- `feature_score` (Float)
- `value_for_money_score` (Float)
- `positive_sentiment_summary` (Text)
- `negative_sentiment_summary` (Text)

## Technologies Used

### Backend
- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Database
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: UI framework
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Fetch API**: HTTP client

## Development

### Adding New AI Tools

1. Use the Flask CLI to add tools:
   ```bash
   flask shell
   ```
   
2. In the shell:
   ```python
   from app.models import AITool
   from app import db
   
   new_tool = AITool(
       name="New AI Tool",
       website="https://example.com",
       short_description="Description here",
       pricing_model="Freemium",
       primary_use_case="Content Creation"
   )
   db.session.add(new_tool)
   db.session.commit()
   ```

### Environment Variables

Create a `.env` file in the backend directory:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/insight_engine
FLASK_ENV=development
FLASK_DEBUG=1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details 