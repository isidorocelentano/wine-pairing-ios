import React, { useState, useContext } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { AlertCircle, CheckCircle, Gift } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config/api';

const CouponPage = () => {
  const [couponCode, setCouponCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();

  const handleRedeem = async (e) => {
    e.preventDefault();
    
    if (!user) {
      navigate('/login');
      return;
    }

    setIsLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/coupon/redeem`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ code: couponCode.trim() }),
      });

      const data = await response.json();
      setResult(data);

      if (data.success) {
        // Refresh user data to show new plan
        await refreshUser();
        setCouponCode('');
      }
    } catch (error) {
      setResult({
        success: false,
        message: 'Fehler beim Einlösen des Gutscheins'
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Gift className="h-6 w-6" />
              Gutschein einlösen
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">
              Sie müssen angemeldet sein, um einen Gutschein einzulösen.
            </p>
            <Button onClick={() => navigate('/login')} className="w-full">
              Zur Anmeldung
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Gift className="h-6 w-6" />
            Gutschein einlösen
          </CardTitle>
          <p className="text-gray-600">
            Lösen Sie Ihren Early Adopter Gutschein ein und erhalten Sie 1 Jahr kostenlosen Pro-Zugang!
          </p>
        </CardHeader>
        <CardContent>
          {user.plan === 'pro' && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <div className="flex items-center gap-2 text-green-700">
                <CheckCircle className="h-5 w-5" />
                <span className="font-medium">Sie haben bereits Pro-Zugang!</span>
              </div>
              <p className="text-green-600 text-sm mt-1">
                Ihr Pro-Plan ist aktiv und Sie können alle Features nutzen.
              </p>
            </div>
          )}

          <form onSubmit={handleRedeem} className="space-y-4">
            <div>
              <label htmlFor="couponCode" className="block text-sm font-medium text-gray-700 mb-2">
                Gutschein-Code
              </label>
              <Input
                id="couponCode"
                type="text"
                placeholder="z.B. WINE-XXXX-XXXX-XXXX"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                className="text-center text-lg font-mono"
                disabled={isLoading}
              />
              <p className="text-sm text-gray-500 mt-1">
                Geben Sie Ihren 12-stelligen Gutschein-Code ein
              </p>
            </div>

            <Button 
              type="submit" 
              className="w-full" 
              disabled={isLoading || !couponCode.trim()}
            >
              {isLoading ? 'Wird eingelöst...' : 'Gutschein einlösen'}
            </Button>
          </form>

          {result && (
            <div className={`mt-6 p-4 rounded-lg ${
              result.success 
                ? 'bg-green-50 border border-green-200' 
                : 'bg-red-50 border border-red-200'
            }`}>
              <div className={`flex items-start gap-2 ${
                result.success ? 'text-green-700' : 'text-red-700'
              }`}>
                {result.success ? (
                  <CheckCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                ) : (
                  <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                )}
                <div>
                  <p className="font-medium">
                    {result.success ? 'Erfolg!' : 'Fehler'}
                  </p>
                  <p className="text-sm mt-1">
                    {result.message}
                  </p>
                  {result.success && result.expires_at && (
                    <p className="text-sm mt-2">
                      Ihr Pro-Plan ist gültig bis: {new Date(result.expires_at).toLocaleDateString('de-DE')}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-medium text-blue-900 mb-2">Was beinhaltet Pro?</h3>
            <ul className="text-blue-700 text-sm space-y-1">
              <li>• Unbegrenzte Wein-Pairings pro Tag</li>
              <li>• Unbegrenzte Chat-Nachrichten</li>
              <li>• Unbegrenzter Weinkeller</li>
              <li>• Unbegrenzte Favoriten</li>
              <li>• Priority Support</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CouponPage;