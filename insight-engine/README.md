# Insight Engine

A comprehensive review aggregator and insights platform for brands and products across all industries, providing deep analytics and sentiment analysis.

## 🚀 Features

### Multi-Industry Platform
- **Review Aggregation**: Collect and analyze reviews from multiple sources for any product category
- **Sentiment Analysis**: AI-powered sentiment analysis and insights across industries
- **Real-Time Integration**: Live review collection from Reddit, social media, and other sources
- **Insight Generation**: Automated key insights and trend analysis for any brand or product

### Current Categories
- **AI Tools Platform**: Software and AI platform analysis
- **Luxury Appliances Dashboard**: Premium appliance brand sentiment and design insights

### Future Categories
- Consumer Electronics
- Fashion & Beauty
- Automotive
- Food & Beverage
- Healthcare & Wellness
- Travel & Hospitality
- And many more...

## 🏗️ Architecture

```
insight-engine/
├── backend/                 # Flask API server
│   ├── project/            # Modular Flask application
│   │   ├── api/           # API blueprints
│   │   └── models/        # Database models
│   ├── config.py          # Configuration management
│   └── run.py             # Application entry point
└── frontend/              # React application
    ├── src/
    │   ├── components/    # React components
    │   ├── pages/         # Page components
    │   └── services/      # API services
    └── public/            # Static assets
```

## 🛠️ Technology Stack

### Backend
- **Python 3.13+**
- **Flask**: Web framework
- **SQLAlchemy**: ORM and database management
- **Flask-Migrate**: Database migrations
- **PRAW**: Reddit API integration
- **TextBlob**: Sentiment analysis
- **BeautifulSoup4**: Web scraping

### Frontend
- **React 18**
- **React Router**: Navigation
- **Tailwind CSS**: Styling
- **Fetch API**: HTTP requests

### Database
- **SQLite**: Development database
- **PostgreSQL**: Production database (configurable)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd insight-engine/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   flask init-db
   ```

5. **Seed sample data**:
   ```bash
   flask seed-ai-tools
   flask seed-luxury-appliances
   flask seed-reviews
   ```

6. **Start the server**:
   ```bash
   python run.py
   ```

The backend API will be available at `http://localhost:5001`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd insight-engine/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 📊 API Endpoints

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

## 🗄️ Database Models

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

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///insight_engine.db
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
REDDIT_USER_AGENT=InsightEngine/1.0
```

### Reddit API Setup
1. Create a Reddit application at https://www.reddit.com/prefs/apps
2. Add your credentials to the `.env` file
3. See `backend/REDDIT_SETUP.md` for detailed instructions

## 🧪 Development

### Backend CLI Commands
- `flask init-db` - Initialize database tables
- `flask seed-ai-tools` - Seed sample AI tools
- `flask seed-luxury-appliances` - Seed sample luxury appliances
- `flask seed-reviews` - Seed sample aggregated reviews

### Frontend Development
- The frontend uses React with modern hooks and functional components
- Tailwind CSS for styling
- API service layer for backend communication

## 📈 Features in Development

- **Category Expansion**: Adding new product categories and industries
- **Advanced Analytics**: More sophisticated insight generation
- **Real-time Updates**: WebSocket integration for live data
- **User Authentication**: User accounts and preferences
- **Export Functionality**: Data export in various formats
- **Mobile App**: React Native mobile application
- **Multi-Source Integration**: Additional review sources beyond Reddit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue on GitHub or contact the development team. 