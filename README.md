# Project Insights

A comprehensive review aggregator and insights platform for brands and products across all industries.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Fork & Clone
```bash
# Fork this repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/project-insights.git
cd project-insights
```

### Backend Setup
```bash
cd insight-engine/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask init-db

# Seed sample data
flask seed-ai-tools
flask seed-luxury-appliances
flask seed-reviews

# Start the server
python run.py
```

The backend API will be available at `http://localhost:5001`

### Frontend Setup
```bash
cd insight-engine/frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
project-insights/
└── insight-engine/
    ├── backend/          # Flask API server
    │   ├── project/     # Modular Flask application
    │   ├── config.py    # Configuration
    │   └── run.py       # Entry point
    └── frontend/        # React application
        ├── src/         # React components
        └── public/      # Static assets
```

## 🔧 Features

- **Multi-Industry Platform**: Review aggregation and sentiment analysis for any brand or product category
- **AI-Powered Insights**: Automated sentiment analysis and trend detection
- **Real-Time Data**: Live review collection from multiple sources
- **Modern UI**: React with Tailwind CSS
- **Scalable Architecture**: Designed to support any product category

## 📊 Current Categories

**Phase 1 Launch Categories:**
- **AI Tools**: Software and AI platforms
- **Luxury Appliances**: Premium kitchen and home appliances

**Future Categories:**
- Consumer Electronics
- Fashion & Beauty
- Automotive
- Food & Beverage
- And many more...

## 📊 API Endpoints

- `GET /health` - Server health
- `GET /api/ai-tools` - AI tools with insights
- `GET /api/luxury-appliances` - Luxury appliances with insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please open an issue on GitHub.
