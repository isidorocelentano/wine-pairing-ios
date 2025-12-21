import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

const AuthCallbackPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { handleOAuthCallback } = useAuth();
  const [status, setStatus] = useState('processing'); // processing, success, error

  useEffect(() => {
    const processCallback = async () => {
      const sessionId = searchParams.get('session_id');
      
      if (!sessionId) {
        setStatus('error');
        setTimeout(() => navigate('/'), 3000);
        return;
      }
      
      const success = await handleOAuthCallback(sessionId);
      
      if (success) {
        setStatus('success');
        setTimeout(() => navigate('/'), 1500);
      } else {
        setStatus('error');
        setTimeout(() => navigate('/'), 3000);
      }
    };
    
    processCallback();
  }, [searchParams, handleOAuthCallback, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-4">
        {status === 'processing' && (
          <>
            <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
            <p className="text-lg text-muted-foreground">Anmeldung wird verarbeitet...</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <CheckCircle className="h-12 w-12 text-green-500 mx-auto" />
            <p className="text-lg text-foreground">Erfolgreich angemeldet!</p>
            <p className="text-sm text-muted-foreground">Sie werden weitergeleitet...</p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <XCircle className="h-12 w-12 text-red-500 mx-auto" />
            <p className="text-lg text-foreground">Anmeldung fehlgeschlagen</p>
            <p className="text-sm text-muted-foreground">Sie werden zur Startseite weitergeleitet...</p>
          </>
        )}
      </div>
    </div>
  );
};

export default AuthCallbackPage;
