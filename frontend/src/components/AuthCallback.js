import React, { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import { API_URL } from '@/config/api';
import { useAuth } from '@/contexts/AuthContext';

/**
 * AuthCallback Component
 * 
 * REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
 * 
 * Handles the callback from Emergent Google Auth.
 * Processes the session_id from URL fragment and exchanges it for user data.
 */
const AuthCallback = () => {
  const navigate = useNavigate();
  const hasProcessed = useRef(false);
  const { refreshAuth } = useAuth();

  useEffect(() => {
    // Prevent double processing (StrictMode)
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      try {
        // Extract session_id from URL fragment
        const hash = window.location.hash;
        const sessionIdMatch = hash.match(/session_id=([^&]+)/);
        
        if (!sessionIdMatch) {
          console.error('No session_id found in URL');
          navigate('/login', { replace: true });
          return;
        }

        const sessionId = sessionIdMatch[1];
        console.log('Processing Google auth session...');

        // Exchange session_id for user data via our backend
        const response = await fetch(`${API_URL}/api/auth/google/session`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ session_id: sessionId })
        });

        if (!response.ok) {
          const error = await response.json();
          console.error('Google auth failed:', error);
          navigate('/login', { 
            replace: true, 
            state: { error: error.detail || 'Google-Anmeldung fehlgeschlagen' } 
          });
          return;
        }

        const userData = await response.json();
        console.log('Google auth successful:', userData.email);

        // Store token in localStorage for Safari/iOS compatibility
        if (userData.token) {
          try {
            localStorage.setItem('wine_auth_token', userData.token);
            console.log('Token stored in localStorage');
          } catch (e) {
            console.warn('Could not store token in localStorage');
          }
        }

        // Refresh auth context to pick up the new token
        if (refreshAuth) {
          await refreshAuth();
        }

        // Navigate to cellar or pairing page
        navigate('/pairing', { replace: true });

      } catch (error) {
        console.error('Auth callback error:', error);
        navigate('/login', { 
          replace: true, 
          state: { error: 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.' } 
        });
      }
    };

    processAuth();
  }, [navigate, refreshAuth]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
        <p className="text-muted-foreground">Anmeldung wird verarbeitet...</p>
      </div>
    </div>
  );
};

export default AuthCallback;
