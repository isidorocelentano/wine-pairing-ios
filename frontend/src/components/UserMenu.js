import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { User, LogOut, Crown, CreditCard } from 'lucide-react';

const UserMenu = () => {
  const { user, isAuthenticated, isPro, logout, getRemainingUsage } = useAuth();
  const { language } = useLanguage();
  const navigate = useNavigate();
  const lang = language || 'de';

  if (!isAuthenticated) {
    return (
      <Button 
        variant="outline" 
        size="sm" 
        onClick={() => navigate('/login')}
        className="gap-2 bg-background/80 backdrop-blur-sm"
      >
        <User className="h-4 w-4" />
        <span className="hidden sm:inline">
          {lang === 'de' ? 'Anmelden' : lang === 'en' ? 'Sign in' : 'Connexion'}
        </span>
      </Button>
    );
  }

  const pairingUsage = getRemainingUsage('pairing');
  const chatUsage = getRemainingUsage('chat');

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="gap-2 px-2 bg-background/80 backdrop-blur-sm">
          {user?.picture ? (
            <img 
              src={user.picture} 
              alt={user.name} 
              className="h-7 w-7 rounded-full"
            />
          ) : (
            <div className="h-7 w-7 rounded-full bg-primary/20 flex items-center justify-center">
              <span className="text-xs font-medium text-primary">
                {user?.name?.charAt(0)?.toUpperCase() || 'U'}
              </span>
            </div>
          )}
          {isPro && (
            <Crown className="h-4 w-4 text-yellow-500" />
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium">{user?.name}</p>
            <p className="text-xs text-muted-foreground">{user?.email}</p>
            <Badge 
              variant={isPro ? "default" : "secondary"} 
              className={`w-fit mt-1 ${isPro ? 'bg-yellow-500/20 text-yellow-600' : ''}`}
            >
              {isPro ? (
                <><Crown className="h-3 w-3 mr-1" /> Pro</>
              ) : (
                'Basic'
              )}
            </Badge>
          </div>
        </DropdownMenuLabel>
        
        {!isPro && (
          <>
            <DropdownMenuSeparator />
            <div className="px-2 py-1.5 text-xs text-muted-foreground">
              <div className="flex justify-between mb-1">
                <span>{lang === 'de' ? 'Pairings heute' : 'Pairings today'}</span>
                <span>{pairingUsage.used}/{pairingUsage.limit}</span>
              </div>
              <div className="flex justify-between">
                <span>{lang === 'de' ? 'Chat heute' : 'Chat today'}</span>
                <span>{chatUsage.used}/{chatUsage.limit}</span>
              </div>
            </div>
          </>
        )}
        
        <DropdownMenuSeparator />
        
        {!isPro && (
          <DropdownMenuItem onClick={() => navigate('/subscription')}>
            <Crown className="mr-2 h-4 w-4 text-yellow-500" />
            <span>{lang === 'de' ? 'Auf Pro upgraden' : 'Upgrade to Pro'}</span>
          </DropdownMenuItem>
        )}
        
        {isPro && (
          <DropdownMenuItem onClick={() => navigate('/subscription')}>
            <CreditCard className="mr-2 h-4 w-4" />
            <span>{lang === 'de' ? 'Abo verwalten' : 'Manage subscription'}</span>
          </DropdownMenuItem>
        )}
        
        <DropdownMenuSeparator />
        
        <DropdownMenuItem onClick={logout} className="text-red-600">
          <LogOut className="mr-2 h-4 w-4" />
          <span>{lang === 'de' ? 'Abmelden' : 'Sign out'}</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default UserMenu;
