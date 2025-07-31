import { base } from '$app/paths';
import { dev } from '$app/environment';

export const load = async ({ fetch, params }) => {
  try {
    // Fetch employee data (always from static JSON)
    const responseJSON = await fetch(base + '/employee.json');
    const dataJSON = await responseJSON.json();
    
    // Fetch top at-risk employees - different URLs for dev vs production
    let topEmployees = [];
    
    if (dev) {
      // Development: fetch from live FastAPI server
      try {
        const topEmployeesResponse = await fetch('http://localhost:8000/top_employees');
        if (topEmployeesResponse.ok) {
          topEmployees = await topEmployeesResponse.json();
        } else {
          console.warn('FastAPI server not responding, using empty array');
        }
      } catch (error) {
        console.warn('Could not connect to FastAPI server:', error);
        // Fallback to empty array in development if server is not running
      }
    } else {
      // Production: fetch from static JSON file
      try {
        const topEmployeesResponse = await fetch(base + '/top_employees.json');
        if (topEmployeesResponse.ok) {
          topEmployees = await topEmployeesResponse.json();
        }
      } catch (error) {
        console.error('Could not load static top employees data:', error);
      }
    }
    
    return { 
      employees: dataJSON,
      topEmployees: topEmployees
    };
  } catch (error) {
    console.error('Error loading data:', error);
    return { 
      employees: [],
      topEmployees: []
    };
  }
};