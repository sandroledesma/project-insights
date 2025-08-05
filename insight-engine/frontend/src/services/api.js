const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

/**
 * API service for communicating with the backend
 */
class ApiService {
  // AI Tools endpoints
  async getAITools() {
    try {
      const response = await fetch(`${API_BASE_URL}/ai-tools`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch AI tools');
      }
    } catch (error) {
      console.error('Error fetching AI tools:', error);
      throw error;
    }
  }

  async getAITool(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai-tools/${id}`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch AI tool');
      }
    } catch (error) {
      console.error('Error fetching AI tool:', error);
      throw error;
    }
  }

  async getRedditReviews(toolId) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai-tools/${toolId}/reddit-reviews`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch Reddit reviews');
      }
    } catch (error) {
      console.error('Error fetching Reddit reviews:', error);
      throw error;
    }
  }

  async refreshReviews(toolId) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai-tools/${toolId}/refresh-reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      if (data.success) {
        return data;
      } else {
        throw new Error(data.error || 'Failed to refresh reviews');
      }
    } catch (error) {
      console.error('Error refreshing reviews:', error);
      throw error;
    }
  }

  // Luxury Appliances endpoints
  async getLuxeAppliances() {
    try {
      const response = await fetch(`${API_BASE_URL}/luxe-appliances`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch luxury appliances');
      }
    } catch (error) {
      console.error('Error fetching luxury appliances:', error);
      throw error;
    }
  }

  async getLuxeAppliance(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/luxe-appliances/${id}`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch luxury appliance');
      }
    } catch (error) {
      console.error('Error fetching luxury appliance:', error);
      throw error;
    }
  }

  async getLuxeReviews(applianceId) {
    try {
      const response = await fetch(`${API_BASE_URL}/luxe-appliances/${applianceId}/reviews`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch luxury appliance reviews');
      }
    } catch (error) {
      console.error('Error fetching luxury appliance reviews:', error);
      throw error;
    }
  }

  async refreshLuxeReviews(applianceId) {
    try {
      const response = await fetch(`${API_BASE_URL}/luxe-appliances/${applianceId}/refresh-reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      if (data.success) {
        return data;
      } else {
        throw new Error(data.error || 'Failed to refresh luxury appliance reviews');
      }
    } catch (error) {
      console.error('Error refreshing luxury appliance reviews:', error);
      throw error;
    }
  }

  async getDesignInsights() {
    try {
      const response = await fetch(`${API_BASE_URL}/luxe-appliances/design-insights`);
      const data = await response.json();
      if (data.success) {
        return data.data;
      } else {
        throw new Error(data.error || 'Failed to fetch design insights');
      }
    } catch (error) {
      console.error('Error fetching design insights:', error);
      throw error;
    }
  }
}

export default new ApiService(); 