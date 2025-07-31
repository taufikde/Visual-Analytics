import { base } from '$app/paths';
import { dev } from '$app/environment';

// API base URL - use local FastAPI in development, static files in production
const API_BASE = dev 
  ? 'http://localhost:8000'  // Your local FastAPI server
  : `${base}`;           // Static JSON files in production

/**
 * Fetch data from API endpoint
 * @param {string} endpoint - The API endpoint (without leading slash)
 * @returns {Promise<any>} - The API response data
 */
export async function apiCall(endpoint) {
  try {
    const url = dev 
      ? `${API_BASE}/${endpoint}`
      : `${API_BASE}/${endpoint}.json`;  // Add .json extension for static files
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`API call failed for endpoint ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Get model information
 */
export async function getModelInfo() {
  return apiCall('model-info');
}

/**
 * Get health status
 */
export async function getHealth() {
  return apiCall('health');
}

/**
 * Get top at-risk employees
 */
export async function getTopEmployees() {
  return apiCall('top_employees');
}

/**
 * Get available API endpoints
 */
export async function getEndpoints() {
  return apiCall('index');
}

// Export the API base for direct use if needed
export { API_BASE };