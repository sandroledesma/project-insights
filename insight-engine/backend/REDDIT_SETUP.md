# Reddit API Setup Guide

To enable Reddit review aggregation, you need to set up Reddit API credentials.

## Step 1: Create a Reddit App

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: InsightEngine (or any name you prefer)
   - **App type**: Select "script"
   - **Description**: AI tool review aggregator
   - **About URL**: Leave blank
   - **Redirect URI**: Leave blank

## Step 2: Get Your Credentials

After creating the app, you'll see:
- **Client ID**: A string under your app name (e.g., "abc123def456")
- **Client Secret**: A longer string (keep this secret!)

## Step 3: Configure Environment Variables

Create a `.env` file in the backend directory with:

```env
# Database Configuration
DATABASE_URL=sqlite:///insight_engine.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1

# Reddit API Configuration
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=InsightEngine/1.0
```

Replace `your_client_id_here` and `your_client_secret_here` with your actual credentials.

## Step 4: Test the Integration

1. Restart your Flask server
2. Go to the frontend and click "Refresh Reddit Reviews" on any AI tool
3. The system will search Reddit for reviews and update the ratings

## How It Works

The Reddit integration:

1. **Searches multiple subreddits** for posts about each AI tool
2. **Analyzes sentiment** of post titles and content using TextBlob
3. **Aggregates reviews** to create overall ratings and summaries
4. **Updates the database** with new review data
5. **Provides sentiment summaries** showing positive and negative feedback

## Supported Subreddits

The system searches these subreddits for AI tool reviews:
- r/artificial
- r/MachineLearning
- r/datascience
- r/programming
- r/technology
- r/startups
- r/ChatGPT
- r/OpenAI
- r/AI
- r/artificialintelligence

## Rate Limiting

Reddit API has rate limits. The system is designed to:
- Search multiple subreddits efficiently
- Handle rate limiting gracefully
- Cache results to avoid repeated API calls

## Troubleshooting

If you get errors:

1. **Check your credentials** - Make sure they're correct in `.env`
2. **Verify app type** - Must be "script" type
3. **Check network** - Ensure your server can reach Reddit API
4. **Review logs** - Check Flask server logs for detailed error messages

## Security Notes

- Never commit your Reddit credentials to version control
- Keep your client secret secure
- The app uses "script" type which is appropriate for server-side applications 