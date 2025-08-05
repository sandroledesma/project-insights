# Insight-Engine Frontend

React-based frontend for the Insight-Engine AI platform review aggregator.

## Features

- **Modern UI**: Built with React and Tailwind CSS
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Search & Filter**: Advanced filtering by use case, pricing model, and ratings
- **Star Ratings**: Visual star rating display
- **Clean Navigation**: Intuitive navigation between pages

## Setup Instructions

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── components/         # Reusable components
│   │   ├── Header.js      # Navigation header
│   │   └── ToolCard.js    # AI tool display card
│   ├── pages/             # Page components
│   │   ├── AIToolList.js  # Main tools listing page
│   │   └── ComparisonPage.js # Comparison page (placeholder)
│   ├── services/          # API services
│   │   └── api.js         # Backend API communication
│   ├── App.js             # Main app component
│   ├── index.js           # React entry point
│   └── index.css          # Global styles with Tailwind
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Components

### Header
Navigation component with logo and menu items.

**Features:**
- Responsive navigation
- Active page highlighting
- Clean, modern design

### ToolCard
Displays individual AI tool information.

**Features:**
- Star rating display
- Tool information (name, description, website)
- Pricing and use case tags
- Hover effects

### AIToolList
Main page displaying all AI tools.

**Features:**
- Search functionality
- Filter by use case and pricing model
- Responsive grid layout
- Loading and error states

### ComparisonPage
Placeholder for future comparison functionality.

## API Integration

The frontend communicates with the backend through the `api.js` service:

```javascript
import apiService from '../services/api';

// Get all tools
const tools = await apiService.getAITools();

// Get specific tool
const tool = await apiService.getAITool(toolId);
```

### Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## Styling

The project uses Tailwind CSS for styling:

- **Utility-first approach**: Rapid development with utility classes
- **Responsive design**: Mobile-first responsive design
- **Custom theme**: Primary color scheme defined in `tailwind.config.js`
- **Component-based**: Reusable component styles

## Development

### Adding New Components

1. Create a new file in `src/components/`
2. Export the component as default
3. Import and use in pages

### Adding New Pages

1. Create a new file in `src/pages/`
2. Add the route in `App.js`
3. Add navigation link in `Header.js`

### API Service

To add new API endpoints:

1. Add methods to `src/services/api.js`
2. Use in components with proper error handling
3. Update loading states as needed

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- **Code splitting**: React Router provides automatic code splitting
- **Optimized builds**: Production builds are optimized and minified
- **Lazy loading**: Components are loaded as needed
- **Efficient rendering**: React's virtual DOM for optimal updates

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Ensure backend is running on `http://localhost:5000`
   - Check CORS settings in backend
   - Verify API endpoints are correct

2. **Build Errors**
   - Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
   - Check for syntax errors in components
   - Verify all imports are correct

3. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check `tailwind.config.js` for content paths
   - Verify PostCSS configuration

### Development Tips

- Use React Developer Tools for debugging
- Check browser console for errors
- Use network tab to debug API calls
- Test responsive design on different screen sizes 