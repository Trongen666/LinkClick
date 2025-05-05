// import { createContext, useState, useEffect, useContext } from 'react';
// import { authApi } from '../services/api.ts';

// // Create context
// export const AuthContext = createContext(null);

// // Auth context provider component
// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   // Check if user is authenticated on mount
//   useEffect(() => {
//     const checkAuth = async () => {
//       const token = localStorage.getItem('auth_token');
//       if (!token) {
//         setLoading(false);
//         return;
//       }

//       try {
//         const userData = await authApi.getCurrentUser();
//         setUser(userData);
//       } catch (err) {
//         console.error('Auth check failed:', err);
//         localStorage.removeItem('auth_token');
//       } finally {
//         setLoading(false);
//       }
//     };

//     checkAuth();
//   }, []);

//   // Login with password
//   const loginWithPassword = async (username, password) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await authApi.loginWithPassword(username, password);
//       localStorage.setItem('auth_token', data.access_token);
//       setUser(data.user);
//       return data;
//     } catch (err) {
//       console.error('Password login failed:', err);
//       const message = err.response?.data?.detail || 'Login failed';
//       setError(message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Login with face
//   const loginWithFace = async (username, faceImage) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await authApi.loginWithFace(username, faceImage);
      
//       // Check if login was successful
//       if (data.access_token) {
//         localStorage.setItem('auth_token', data.access_token);
//         setUser(data.user);
//       }
      
//       return data;
//     } catch (err) {
//       console.error('Face login failed:', err);
//       const message = err.response?.data?.detail || 'Face login failed';
//       setError(message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Login with OTP
//   const loginWithOTP = async (username, otp) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await authApi.loginWithOTP(username, otp);
      
//       // Check if login was successful
//       if (data.access_token) {
//         localStorage.setItem('auth_token', data.access_token);
//         setUser(data.user);
//       }
      
//       return data;
//     } catch (err) {
//       console.error('OTP login failed:', err);
//       const message = err.response?.data?.detail || 'OTP verification failed';
//       setError(message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Register new user
//   const register = async (userData) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const data = await authApi.register(userData);
//       return data;
//     } catch (err) {
//       console.error('Registration failed:', err);
//       const message = err.response?.data?.detail || 'Registration failed';
//       setError(message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Update user's face
//   const updateFace = async (faceImage) => {
//     setLoading(true);
//     setError(null);
    
//     try {
//       const updatedUser = await authApi.updateFace(faceImage);
//       setUser(updatedUser);
//       return updatedUser;
//     } catch (err) {
//       console.error('Face update failed:', err);
//       const message = err.response?.data?.detail || 'Failed to update face';
//       setError(message);
//       throw err;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Logout
//   const logout = () => {
//     localStorage.removeItem('auth_token');
//     setUser(null);
//   };

//   // Context value
//   const value = {
//     user,
//     loading,
//     error,
//     loginWithPassword,
//     loginWithFace,
//     loginWithOTP,
//     register,
//     updateFace,
//     logout,
//     isAuthenticated: !!user,
//   };

//   return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
// };

// // Custom hook to use auth context
// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };

import React, {
    createContext,
    useState,
    useEffect,
    useContext,
    ReactNode,
  } from 'react';
  import { authApi } from '../services/api';
  
  // Define types for user and API responses
  export interface User {
    id: string;
    username: string;
    email?: string;
    // Add other fields as needed
  }
  
  export interface AuthResponse {
    access_token: string;
    user: User;
  }
  
  interface AuthContextType {
    user: User | null;
    loading: boolean;
    error: string | null;
    loginWithPassword: (username: string, password: string) => Promise<AuthResponse>;
    loginWithFace: (username: string, faceImage: Blob | string) => Promise<AuthResponse>;
    loginWithOTP: (username: string, otp: string) => Promise<AuthResponse>;
    register: (userData: Record<string, any>) => Promise<any>;
    updateFace: (faceImage: Blob | string) => Promise<User>;
    logout: () => void;
    isAuthenticated: boolean;
  }
  
  interface AuthProviderProps {
    children: ReactNode;
  }
  
  // Create context
  export const AuthContext = createContext<AuthContextType | null>(null);
  
  // Auth provider
  export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
  
    useEffect(() => {
      const checkAuth = async () => {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          setLoading(false);
          return;
        }
  
        try {
          const userData = await authApi.getCurrentUser();
          setUser(userData as User);
        } catch (err: unknown) {
          console.error('Auth check failed:', err);
          localStorage.removeItem('auth_token');
        } finally {
          setLoading(false);
        }
      };
  
      checkAuth();
    }, []);
  
    const loginWithPassword = async (
      username: string,
      password: string
    ): Promise<AuthResponse> => {
      setLoading(true);
      setError(null);
      try {
        const data = await authApi.loginWithPassword(username, password);
        localStorage.setItem('auth_token', data.access_token);
        setUser(data.user);
        return data;
      } catch (err: unknown) {
        console.error('Password login failed:', err);
        const message = (err as any).response?.data?.detail || 'Login failed';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    };
  
    const loginWithFace = async (
      username: string,
      faceImage: Blob | string
    ): Promise<AuthResponse> => {
      setLoading(true);
      setError(null);
      try {
        const data = await authApi.loginWithFace(username, faceImage);
        if (data.access_token) {
          localStorage.setItem('auth_token', data.access_token);
          setUser(data.user);
        }
        return data;
      } catch (err: unknown) {
        console.error('Face login failed:', err);
        const message = (err as any).response?.data?.detail || 'Face login failed';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    };
  
    const loginWithOTP = async (
      username: string,
      otp: string
    ): Promise<AuthResponse> => {
      setLoading(true);
      setError(null);
      try {
        const data = await authApi.loginWithOTP(username, otp);
        if (data.access_token) {
          localStorage.setItem('auth_token', data.access_token);
          setUser(data.user);
        }
        return data;
      } catch (err: unknown) {
        console.error('OTP login failed:', err);
        const message = (err as any).response?.data?.detail || 'OTP verification failed';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    };
  
    const register = async (userData: Record<string, any>): Promise<any> => {
      setLoading(true);
      setError(null);
      try {
        const data = await authApi.register(userData);
        return data;
      } catch (err: unknown) {
        console.error('Registration failed:', err);
        const message = (err as any).response?.data?.detail || 'Registration failed';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    };
  
    const updateFace = async (faceImage: Blob | string): Promise<User> => {
      setLoading(true);
      setError(null);
      try {
        const updatedUser = await authApi.updateFace(faceImage);
        setUser(updatedUser);
        return updatedUser;
      } catch (err: unknown) {
        console.error('Face update failed:', err);
        const message = (err as any).response?.data?.detail || 'Failed to update face';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    };
  
    const logout = () => {
      localStorage.removeItem('auth_token');
      setUser(null);
    };
  
    const value: AuthContextType = {
      user,
      loading,
      error,
      loginWithPassword,
      loginWithFace,
      loginWithOTP,
      register,
      updateFace,
      logout,
      isAuthenticated: !!user,
    };
  
    return (
      <AuthContext.Provider value={value}>
        {children}
      </AuthContext.Provider>
    );
  };
  
  // Hook
  export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) {
      throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
  };
  