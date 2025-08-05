const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

/**
 * API service for communicating with the backend
 */
class ApiService {
  /**
   * Fetch all AI tools from the backend
   * @returns {Promise<Array>} Array of AI tools
   */
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

  /**
   * Fetch a single AI tool by ID
   * @param {number} toolId - The ID of the AI tool
   * @returns {Promise<Object>} AI tool data with aggregated review
   */
  async getAITool(toolId) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai-tools/${toolId}`);
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

  /**
   * Fetch Reddit reviews for a specific AI tool
   * @param {number} toolId - The ID of the AI tool
   * @returns {Promise<Object>} Reddit reviews and aggregated data
   */
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

  /**
   * Refresh Reddit reviews for a specific AI tool
   * @param {number} toolId - The ID of the AI tool
   * @returns {Promise<Object>} Refresh result
   */
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
}

export default new ApiService(); 