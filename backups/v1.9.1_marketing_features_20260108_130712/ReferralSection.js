import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API } from '@/config/api';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Gift, 
  Copy, 
  Check, 
  Users, 
  Share2, 
  Trophy,
  Sparkles
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import ShareButtons from './ShareButtons';

const ReferralSection = () => {
  const { user, token } = useAuth();
  const [referralData, setReferralData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [applyCode, setApplyCode] = useState('');
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    if (user && token) {
      fetchReferralData();
    }
  }, [user, token]);

  const fetchReferralData = async () => {
    try {
      const response = await axios.get(`${API}/referral/my-code`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReferralData(response.data);
    } catch (error) {
      console.error('Error fetching referral data:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyReferralLink = async () => {
    if (referralData?.referral_link) {
      try {
        await navigator.clipboard.writeText(referralData.referral_link);
        setCopied(true);
        toast.success('Link kopiert!');
        setTimeout(() => setCopied(false), 2000);
      } catch (err) {
        toast.error('Kopieren fehlgeschlagen');
      }
    }
  };

  const copyReferralCode = async () => {
    if (referralData?.referral_code) {
      try {
        await navigator.clipboard.writeText(referralData.referral_code);
        toast.success('Code kopiert!');
      } catch (err) {
        toast.error('Kopieren fehlgeschlagen');
      }
    }
  };

  const handleApplyCode = async () => {
    if (!applyCode.trim()) return;
    
    setApplying(true);
    try {
      const response = await axios.post(
        `${API}/referral/apply`,
        { referral_code: applyCode.trim() },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(response.data.message);
      setApplyCode('');
      fetchReferralData(); // Refresh data
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Fehler beim Anwenden des Codes');
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return (
      <Card className="animate-pulse">
        <CardHeader>
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
        </CardHeader>
        <CardContent>
          <div className="h-20 bg-gray-200 rounded"></div>
        </CardContent>
      </Card>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Main Referral Card */}
      <Card className="border-2 border-wine-200 bg-gradient-to-br from-wine-50/50 to-amber-50/50">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-wine-100 rounded-full">
              <Gift className="w-6 h-6 text-wine-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Freunde einladen</CardTitle>
              <CardDescription>
                Teile Wine Pairing und erhalte Belohnungen!
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Reward Info */}
          <div className="bg-white rounded-lg p-4 border border-wine-100">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-amber-500 mt-0.5" />
              <div>
                <p className="font-medium text-gray-900">So funktioniert's:</p>
                <p className="text-sm text-gray-600 mt-1">
                  {referralData?.reward_info?.description || 
                   'Du und dein Freund erhalten jeweils 1 Monat Pro gratis, wenn sich dein Freund registriert und ein Pro-Abo abschließt!'}
                </p>
              </div>
            </div>
          </div>

          {/* Referral Code */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Dein persönlicher Empfehlungscode
            </label>
            <div className="flex gap-2">
              <div className="flex-1 bg-gray-100 rounded-lg px-4 py-3 font-mono text-lg font-bold text-wine-700 tracking-wider">
                {referralData?.referral_code || '---'}
              </div>
              <Button 
                variant="outline" 
                size="icon"
                onClick={copyReferralCode}
                className="h-12 w-12"
              >
                <Copy className="w-5 h-5" />
              </Button>
            </div>
          </div>

          {/* Referral Link */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Oder teile diesen Link direkt
            </label>
            <div className="flex gap-2">
              <Input 
                value={referralData?.referral_link || ''} 
                readOnly 
                className="font-mono text-sm"
              />
              <Button 
                variant={copied ? "default" : "outline"}
                onClick={copyReferralLink}
                className={copied ? "bg-green-600 hover:bg-green-700" : ""}
              >
                {copied ? <Check className="w-4 h-4 mr-2" /> : <Copy className="w-4 h-4 mr-2" />}
                {copied ? 'Kopiert!' : 'Kopieren'}
              </Button>
            </div>
          </div>

          {/* Share Buttons */}
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">
              Direkt teilen auf
            </label>
            <ShareButtons 
              url={referralData?.referral_link}
              title="🍷 Entdecke Wine Pairing - Dein KI-Sommelier! Registriere dich mit meinem Link und erhalte 1 Monat Pro gratis!"
              hashtags="WeinPairing,Wein,KI,Sommelier"
              size="md"
            />
          </div>
        </CardContent>
      </Card>

      {/* Stats Card */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-500" />
            Deine Erfolge
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-wine-600">
                {referralData?.referral_count || 0}
              </div>
              <div className="text-sm text-gray-600">Freunde eingeladen</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 text-center">
              <div className="text-3xl font-bold text-green-600">
                {referralData?.bonus_months_earned || 0}
              </div>
              <div className="text-sm text-gray-600">Bonus-Monate verdient</div>
            </div>
          </div>

          {/* Referred Users List */}
          {referralData?.referred_users?.length > 0 && (
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Eingeladene Freunde:</p>
              <div className="space-y-2">
                {referralData.referred_users.map((u, idx) => (
                  <div key={idx} className="flex items-center justify-between bg-gray-50 rounded px-3 py-2 text-sm">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-gray-400" />
                      <span>{u.name || u.email}</span>
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded ${
                      u.plan === 'pro' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                    }`}>
                      {u.plan === 'pro' ? 'Pro' : 'Basic'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Apply Code Card (if user hasn't been referred yet) */}
      {!referralData?.referred_by && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Hast du einen Empfehlungscode?</CardTitle>
            <CardDescription>
              Gib den Code eines Freundes ein und erhalte Belohnungen!
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2">
              <Input 
                value={applyCode}
                onChange={(e) => setApplyCode(e.target.value.toUpperCase())}
                placeholder="z.B. WP1A2B3C4D"
                className="font-mono"
                maxLength={10}
              />
              <Button 
                onClick={handleApplyCode}
                disabled={!applyCode.trim() || applying}
              >
                {applying ? 'Wird angewendet...' : 'Anwenden'}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ReferralSection;
