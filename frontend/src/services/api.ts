// import axios from 'axios';

// // Create axios instance with defaults
// const api = axios.create({
//   baseURL: '/api/v1'
// });

// // Add auth token to requests if available
// api.interceptors.request.use(config => {
//   const token = localStorage.getItem('auth_token');
//   if (token) {
//     config.headers['Authorization'] = `Bearer ${token}`;
//   }
//   return config;
// });

// // Handle response errors
// api.interceptors.response.use(
//   response => response,
//   error => {
//     if (error.response && error.response.status === 401) {
//       // Unauthorized, clear token and redirect to login
//       localStorage.removeItem('auth_token');
//       window.location.href = '/login';
//     }
//     return Promise.reject(error);
//   }
// );

// // Auth API methods
// export const authApi = {
//   // Register a new user
//   register: async (userData) => {
//     const response = await api.post('/auth/register', userData);
//     return response.data;
//   },

//   // Login with username and password
//   loginWithPassword: async (username, password) => {
//     const formData = new FormData();
//     formData.append('username', username);
//     formData.append('password', password);
    
//     const response = await api.post('/auth/login/password', formData);
//     return response.data;
//   },

//   // Login with face recognition
//   loginWithFace: async (username, faceImage) => {
//     const formData = new FormData();
//     formData.append('username', username);
//     formData.append('face_image', faceImage);
    
//     const response = await api.post('/auth/login/face', formData);
//     return response.data;
//   },

//   // Login with OTP
//   loginWithOTP: async (username, otp) => {
//     const response = await api.post('/auth/login/otp', { username, otp });
//     return response.data;
//   },

//   // Get current user details
//   getCurrentUser: async () => {
//     const response = await api.get('/auth/me');
//     return response.data;
//   },

//   // Update user's face for authentication
//   updateFace: async (faceImage) => {
//     const formData = new FormData();
//     formData.append('face_image', faceImage);
    
//     const response = await api.post('/auth/update-face', formData);
//     return response.data;
//   },

//   // Get OTP QR code for user
//   getOTPQRCode: async () => {
//     const response = await api.get('/auth/otp-qr-code');
//     return response.data;
//   },
// };

// export default api;

import axios, { AxiosInstance } from 'axios';

// --- Interfaces ---
export interface User {
  id: string;
  username: string;
  email?: string;
  // Add more fields as needed
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

// --- Axios instance ---
const api: AxiosInstance = axios.create({
  baseURL: '/api/v1',
});

// --- Request interceptor ---
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// --- Response interceptor ---
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// --- Auth API methods ---
export const authApi = {
  register: async (userData: Record<string, any>): Promise<any> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  loginWithPassword: async (username: string, password: string): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login/password', formData);
    return response.data;
  },

  loginWithFace: async (username: string, faceImage: Blob | string): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('face_image', faceImage);

    const response = await api.post('/auth/login/face', formData);
    return response.data;
  },

  loginWithOTP: async (username: string, otp: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/login/otp', { username, otp });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  updateFace: async (faceImage: Blob | string): Promise<User> => {
    const formData = new FormData();
    formData.append('face_image', faceImage);

    const response = await api.post('/auth/update-face', formData);
    return response.data;
  },

  getOTPQRCode: async (): Promise<{ qr_code_url: string }> => {
    const response = await api.get('/auth/otp-qr-code');
    return response.data;
  },
};

export default api;
