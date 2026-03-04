// API Configuration
// Change this to your deployed API URL

// Local development
// export const API_URL = 'http://localhost:3001';

// Production - Update this after deploying the API
export const API_URL = process.env.REACT_APP_API_URL || 'https://mhlaba-api.onrender.com';

export const DEFAULT_MODEL = 'llama3.2';
