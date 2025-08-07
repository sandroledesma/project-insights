const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

/**
 * API service for communicating with the unified backend
 */
class ApiService {
  
  // Unified Products endpoints
  
  /**
   * Get all products with optional subcategory filtering
   * @param {string} subcategory - Optional subcategory filter (e.g., 'ai-tools', 'luxury-appliances')
   * @param {number} page - Page number for pagination
   * @param {number} perPage - Items per page
   */
  async getProducts(subcategory = null, page = 1, perPage = 20) {
    try {
      const params = new URLSearchParams();
      if (subcategory) params.append('subcategory', subcategory);
      if (page !== 1) params.append('page', page.toString());
      if (perPage !== 20) params.append('per_page', perPage.toString());
      
      const queryString = params.toString();
      const url = `${API_BASE_URL}/products${queryString ? `?${queryString}` : ''}`;
      
      const response = await fetch(url);
      const data = await response.json();
      
      if (response.ok) {
        return data;
      } else {
        throw new Error(data.message || data.error || 'Failed to fetch products');
      }
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  }

  /**
   * Get a single product by ID with full details
   * @param {number} id - Product ID
   */
  async getProduct(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/products/${id}`);
      const data = await response.json();
      
      if (response.ok) {
        return data;
      } else {
        throw new Error(data.message || data.error || 'Failed to fetch product');
      }
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  }

  /**
   * Get all available categories with subcategories
   */
  async getCategories() {
    try {
      const response = await fetch(`${API_BASE_URL}/products/categories`);
      const data = await response.json();
      
      if (response.ok) {
        return data;
      } else {
        throw new Error(data.message || data.error || 'Failed to fetch categories');
      }
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }

  /**
   * Get all available subcategories
   */
  async getSubcategories() {
    try {
      const response = await fetch(`${API_BASE_URL}/products/subcategories`);
      const data = await response.json();
      
      if (response.ok) {
        return data;
      } else {
        throw new Error(data.message || data.error || 'Failed to fetch subcategories');
      }
    } catch (error) {
      console.error('Error fetching subcategories:', error);
      throw error;
    }
  }

  // Legacy compatibility methods - these maintain the old API for existing components
  
  /**
   * Get AI Tools (legacy compatibility)
   * Maps to products with subcategory='ai-tools'
   */
  async getAITools() {
    try {
      const response = await this.getProducts('ai-tools');
      // Transform the response to match the old format expected by frontend
      // Return just the array, not wrapped in success/data object
      return response.products.map(product => ({
        id: product.id,
        name: product.name,
        website: product.brand, // Using brand as website for now
        short_description: product.short_description,
        pricing_model: this.getAttributeValue(product.attributes, 'Pricing Model') || 'Unknown',
        primary_use_case: this.getAttributeValue(product.attributes, 'Primary Use Case') || 'General',
        insight_snippet: product.insight_snippet,
        ideal_for_tags: this.getAttributeValue(product.attributes, 'Languages Supported') || '',
        overall_rating: product.overall_rating,
        created_at: product.created_at,
        updated_at: product.updated_at,
        // Add aggregated_review for compatibility with sorting
        aggregated_review: product.overall_rating ? { overall_rating: product.overall_rating } : null
      }));
    } catch (error) {
      console.error('Error fetching AI tools:', error);
      throw error;
    }
  }

  /**
   * Get single AI Tool (legacy compatibility)
   */
  async getAITool(id) {
    try {
      const response = await this.getProduct(id);
      const product = response.product;
      
      return {
        success: true,
        data: {
          id: product.id,
          name: product.name,
          website: product.brand,
          short_description: product.short_description,
          pricing_model: this.getAttributeValue(product.attributes, 'Pricing Model') || 'Unknown',
          primary_use_case: this.getAttributeValue(product.attributes, 'Primary Use Case') || 'General',
          insight_snippet: product.insight_snippet,
          ideal_for_tags: this.getAttributeValue(product.attributes, 'Languages Supported') || '',
          overall_rating: product.aggregated_review?.overall_rating,
          created_at: product.created_at,
          updated_at: product.updated_at,
          attributes: product.attributes,
          price_history: product.price_history,
          aggregated_review: product.aggregated_review
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get Luxury Appliances (legacy compatibility)
   * Maps to products with subcategory='luxury-appliances'
   */
  async getLuxeAppliances() {
    try {
      const response = await this.getProducts('luxury-appliances');
      
      // Return just the array, not wrapped in success/data object
      return response.products.map(product => ({
        id: product.id,
        name: product.name,
        brand: product.brand,
        category: product.subcategory_name,
        model_number: this.getAttributeValue(product.attributes, 'Model Number') || '',
        msrp: parseInt(this.getAttributeValue(product.attributes, 'MSRP') || '0'),
        price_range: this.getAttributeValue(product.attributes, 'Price Range') || '',
        website: product.brand,
        description: product.short_description,
        features: this.getAttributeValue(product.attributes, 'Features') || '',
        design_style: this.getAttributeValue(product.attributes, 'Design Style') || '',
        finish_options: this.getAttributeValue(product.attributes, 'Finish Options') || '',
        dimensions: this.getAttributeValue(product.attributes, 'Dimensions') || '',
        energy_rating: this.getAttributeValue(product.attributes, 'Energy Rating') || '',
        warranty: this.getAttributeValue(product.attributes, 'Warranty') || '',
        insight_snippet: product.insight_snippet,
        style_tags: this.getAttributeValue(product.attributes, 'Style Tags') || '',
        overall_rating: product.overall_rating,
        created_at: product.created_at,
        updated_at: product.updated_at,
        // Add aggregated_review for compatibility with sorting
        aggregated_review: product.overall_rating ? { overall_rating: product.overall_rating } : null
      }));
    } catch (error) {
      console.error('Error fetching luxury appliances:', error);
      throw error;
    }
  }

  /**
   * Get single Luxury Appliance (legacy compatibility)
   */
  async getLuxeAppliance(id) {
    try {
      const response = await this.getProduct(id);
      const product = response.product;
      
      return {
        success: true,
        data: {
          id: product.id,
          name: product.name,
          brand: product.brand,
          category: product.subcategory_name,
          model_number: this.getAttributeValue(product.attributes, 'Model Number') || '',
          msrp: parseInt(this.getAttributeValue(product.attributes, 'MSRP') || '0'),
          price_range: this.getAttributeValue(product.attributes, 'Price Range') || '',
          website: product.brand,
          description: product.short_description,
          features: this.getAttributeValue(product.attributes, 'Features') || '',
          design_style: this.getAttributeValue(product.attributes, 'Design Style') || '',
          finish_options: this.getAttributeValue(product.attributes, 'Finish Options') || '',
          dimensions: this.getAttributeValue(product.attributes, 'Dimensions') || '',
          energy_rating: this.getAttributeValue(product.attributes, 'Energy Rating') || '',
          warranty: this.getAttributeValue(product.attributes, 'Warranty') || '',
          insight_snippet: product.insight_snippet,
          style_tags: this.getAttributeValue(product.attributes, 'Style Tags') || '',
          overall_rating: product.aggregated_review?.overall_rating,
          created_at: product.created_at,
          updated_at: product.updated_at,
          attributes: product.attributes,
          price_history: product.price_history,
          aggregated_review: product.aggregated_review
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Helper methods
  
  /**
   * Get attribute value by key from attributes array
   */
  getAttributeValue(attributes, key) {
    if (!attributes || !Array.isArray(attributes)) return null;
    const attribute = attributes.find(attr => attr.key === key);
    return attribute ? attribute.value : null;
  }

  // Placeholder methods for features not yet implemented
  
  async getRedditReviews(productId) {
    console.warn('Reddit reviews not yet implemented in new backend');
    return { success: false, error: 'Feature not yet implemented' };
  }

  async refreshReviews(productId) {
    console.warn('Refresh reviews not yet implemented in new backend');
    return { success: false, error: 'Feature not yet implemented' };
  }

  async getLuxeReviews(productId) {
    try {
      const response = await this.getProduct(productId);
      return {
        success: true,
        data: response.product.aggregated_review || {}
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async refreshLuxeReviews(productId) {
    console.warn('Refresh luxury reviews not yet implemented in new backend');
    return { success: false, error: 'Feature not yet implemented' };
  }

  async getDesignInsights() {
    console.warn('Design insights not yet implemented in new backend');
    return { success: false, error: 'Feature not yet implemented' };
  }
}

export default new ApiService();