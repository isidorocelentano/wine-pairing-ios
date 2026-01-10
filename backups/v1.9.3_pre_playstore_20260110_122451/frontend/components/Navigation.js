import React, { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { Wine, Utensils, MessageCircle, Home, BookOpen, Users, Grape, Heart, Database, Map, UserCog, Menu, X, Gift } from 'lucide-react';
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useLanguage();
  const { isPro, isAuthenticated } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  // Main nav items (6 core items)
  const mainNavItems = [
    { path: '/', icon: Home, labelKey: 'nav_home' },
    { path: '/pairing', icon: Utensils, labelKey: 'nav_pairing' },
    { path: '/cellar', icon: Wine, labelKey: 'nav_cellar' },
    { path: '/feed', icon: Users, labelKey: 'nav_feed' },
    // Weinprofil nur für Pro-User anzeigen
    ...(isPro && isAuthenticated ? [{ path: '/profile', icon: UserCog, labelKey: 'nav_profile', isPro: true }] : []),
    { path: '/chat', icon: MessageCircle, labelKey: 'nav_sommelier', isClaude: true },
  ];

  // Secondary nav items (in burger menu)
  const secondaryNavItems = [
    { path: '/sommelier-kompass', icon: Map, labelKey: 'regional_nav' },
    { path: '/grapes', icon: Grape, labelKey: 'nav_grapes' },
    { path: '/wine-database', icon: Database, labelKey: 'nav_wine_database' },
    { path: '/favorites', icon: Heart, labelKey: 'nav_favorites' },
    { path: '/blog', icon: BookOpen, labelKey: 'nav_blog' },
    { path: '/referral', icon: Gift, labelKey: 'nav_referral' },
  ];

  const handleNavClick = (path) => {
    navigate(path);
    setMenuOpen(false);
  };

  return (
    <>
      {/* Burger Menu Overlay */}
      {menuOpen && (
        <div className="fixed inset-0 bg-black/50 z-[9998]" onClick={() => setMenuOpen(false)} />
      )}
      
      {/* Burger Menu Panel */}
      <div className={`fixed bottom-20 left-4 right-4 md:left-auto md:right-6 md:bottom-24 md:w-64 bg-background rounded-2xl shadow-2xl border z-[9999] transition-all duration-300 ${menuOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-semibold text-muted-foreground">Mehr</span>
            <button onClick={() => setMenuOpen(false)} className="p-1 hover:bg-secondary rounded-full">
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-3 gap-2">
            {secondaryNavItems.map((item) => (
              <button
                key={item.path}
                onClick={() => handleNavClick(item.path)}
                className={`flex flex-col items-center gap-1 p-3 rounded-xl transition-all ${
                  location.pathname === item.path
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-secondary'
                }`}
              >
                <item.icon className="w-5 h-5" strokeWidth={1.5} />
                <span className="text-xs">{t(item.labelKey)}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="nav-dock fixed bottom-0 left-0 right-0 md:left-1/2 md:right-auto md:-translate-x-1/2 md:bottom-6 md:rounded-full rounded-t-2xl px-2 md:px-6 py-2 md:py-3 shadow-2xl z-[9999] md:max-w-none" data-testid="main-navigation">
        <div className="flex items-center justify-center gap-1 md:gap-2">
          {/* Burger Menu Button */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className={`flex items-center justify-center min-w-[44px] h-[44px] rounded-full transition-elegant flex-shrink-0 ${
              menuOpen ? 'bg-primary text-primary-foreground' : 'hover:bg-secondary'
            }`}
          >
            <Menu className="w-5 h-5" strokeWidth={1.5} />
          </button>

          {/* Main Nav Items */}
          {mainNavItems.map((item) => (
            <button
              key={item.path}
              onClick={() => handleNavClick(item.path)}
              data-testid={`nav-${item.labelKey.split('_')[1]}`}
              className={`flex items-center justify-center min-w-[44px] h-[44px] md:px-4 md:gap-2 rounded-full transition-elegant flex-shrink-0 ${
                location.pathname === item.path
                  ? 'bg-primary text-primary-foreground'
                  : 'hover:bg-secondary'
              }`}
            >
              {item.isClaude ? (
                <img
                  src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                  alt="Claude Avatar"
                  className="w-6 h-6 rounded-full border border-border/60 object-cover shadow-sm"
                />
              ) : (
                <item.icon className="w-5 h-5" strokeWidth={1.5} />
              )}
              <span className="hidden md:inline text-sm font-medium">{t(item.labelKey)}</span>
            </button>
          ))}
        </div>
      </nav>
    </>
  );
};

export default Navigation;
