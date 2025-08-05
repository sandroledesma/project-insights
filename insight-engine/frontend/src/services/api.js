const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

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
}

export default new ApiService(); 