import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { CheckCircle, Loader2, Crown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Confetti from 'react-confetti';

const API_URL = process.env.REACT_APP_BACKEND_URL;

const SubscriptionSuccessPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { refreshUser } = useAuth();
  const [status, setStatus] = useState('verifying'); // verifying, success, error
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    const verifyPayment = async () => {
      const sessionId = searchParams.get('session_id');
      
      if (!sessionId) {
        setStatus('error');
        return;
      }
      
      try {
        const response = await fetch(`${API_URL}/api/subscription/status/${sessionId}`, {
          credentials: 'include'
        });
        
        if (!response.ok) {
          setStatus('error');
          return;
        }
        
        const data = await response.json();
        
        if (data.payment_status === 'paid') {
          setStatus('success');
          setShowConfetti(true);
          await refreshUser();
          setTimeout(() => setShowConfetti(false), 5000);
        } else {
          setStatus('error');
        }
      } catch (err) {
        console.error('Payment verification error:', err);
        setStatus('error');
      }
    };
    
    verifyPayment();
  }, [searchParams, refreshUser]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      {showConfetti && <Confetti recycle={false} numberOfPieces={200} />}
      
      <Card className="max-w-md w-full">
        <CardContent className="pt-8 pb-8 text-center">
          {status === 'verifying' && (
            <>
              <Loader2 className="h-16 w-16 animate-spin text-primary mx-auto mb-4" />
              <h1 className="text-2xl font-bold mb-2">Zahlung wird verifiziert...</h1>
              <p className="text-muted-foreground">Bitte warten Sie einen Moment.</p>
            </>
          )}
          
          {status === 'success' && (
            <>
              <div className="relative inline-block mb-4">
                <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
                <Crown className="h-6 w-6 text-yellow-500 absolute -top-1 -right-1" />
              </div>
              <h1 className="text-2xl font-bold mb-2">Willkommen bei Pro! 🎉</h1>
              <p className="text-muted-foreground mb-6">
                Ihre Zahlung war erfolgreich. Sie haben jetzt unbegrenzten Zugang zu allen Features.
              </p>
              <div className="space-y-3">
                <Button onClick={() => navigate('/pairing')} className="w-full">
                  Zum Wein-Pairing
                </Button>
                <Button variant="outline" onClick={() => navigate('/')} className="w-full">
                  Zur Startseite
                </Button>
              </div>
            </>
          )}
          
          {status === 'error' && (
            <>
              <div className="h-16 w-16 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">❌</span>
              </div>
              <h1 className="text-2xl font-bold mb-2">Etwas ist schiefgelaufen</h1>
              <p className="text-muted-foreground mb-6">
                Die Zahlung konnte nicht verifiziert werden. Bitte kontaktieren Sie uns, falls das Problem weiterhin besteht.
              </p>
              <Button onClick={() => navigate('/subscription')} className="w-full">
                Zurück zur Übersicht
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default SubscriptionSuccessPage;
