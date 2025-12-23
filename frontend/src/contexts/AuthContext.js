import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

export const AuthContext = createContext(null);

import { API_URL } from '../config/api';

// Token-Helfer für localStorage (Safari/iOS-kompatibel)
const TOKEN_KEY = 'wine_auth_token';

const getStoredToken = () => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
};

const setStoredToken = (token) => {
  try {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  } catch {
    // localStorage nicht verfügbar
  }
};

const clearStoredToken = () => {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    // Ignore
  }
};

// Auth-Header für API-Aufrufe
export const getAuthHeaders = () => {
  const token = getStoredToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check for existing session on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = getStoredToken();
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      
      const response = await fetch(`${API_URL}/api/auth/me`, {
        credentials: 'include',
        headers
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        setUser(null);
        clearStoredToken();
      }
    } catch (err) {
      console.error('Auth check failed:', err);
      setUser(null);
      clearStoredToken();
    } finally {
      setLoading(false);
    }
  };

  const register = useCallback(async (email, password, name) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password, name })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Registrierung fehlgeschlagen');
      }
      
      setUser(data);
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Anmeldung fehlgeschlagen');
      }
      
      setUser(data);
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await fetch(`${API_URL}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
    }
  }, []);

  const refreshUser = useCallback(async () => {
    await checkAuth();
  }, []);

  const isPro = user?.plan === 'pro';
  
  const getRemainingUsage = useCallback((type) => {
    if (!user) return { used: 0, limit: 5, remaining: 5 };
    if (isPro) return { used: 0, limit: Infinity, remaining: Infinity };
    
    const limits = {
      pairing: { used: user.usage?.pairing_requests_today || 0, limit: 5 },
      chat: { used: user.usage?.chat_messages_today || 0, limit: 5 },
      cellar: { used: 0, limit: 10 },
      favorites: { used: 0, limit: 10 }
    };
    
    const usage = limits[type] || { used: 0, limit: 5 };
    return { ...usage, remaining: Math.max(0, usage.limit - usage.used) };
  }, [user, isPro]);

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    isPro,
    register,
    login,
    logout,
    refreshUser,
    getRemainingUsage,
    clearError: () => setError(null)
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
