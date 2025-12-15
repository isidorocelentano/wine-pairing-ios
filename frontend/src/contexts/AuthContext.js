import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

const API_URL = process.env.REACT_APP_BACKEND_URL;

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
      const response = await fetch(`${API_URL}/api/auth/me`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        setUser(null);
      }
    } catch (err) {
      console.error('Auth check failed:', err);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const loginWithGoogle = useCallback(() => {
    // Redirect to Emergent OAuth
    const currentUrl = window.location.origin;
    const callbackUrl = `${currentUrl}/auth/callback`;
    const oauthUrl = `https://demobackend.emergentagent.com/auth/v1/env/oauth/google?callback_url=${encodeURIComponent(callbackUrl)}`;
    window.location.href = oauthUrl;
  }, []);

  const handleOAuthCallback = useCallback(async (sessionId) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_URL}/api/auth/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ session_id: sessionId })
      });
      
      if (!response.ok) {
        throw new Error('Authentication failed');
      }
      
      const userData = await response.json();
      setUser(userData);
      return true;
    } catch (err) {
      console.error('OAuth callback error:', err);
      setError(err.message);
      return false;
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
      cellar: { used: 0, limit: 10 }, // Will be fetched separately
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
    loginWithGoogle,
    handleOAuthCallback,
    logout,
    refreshUser,
    getRemainingUsage
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
