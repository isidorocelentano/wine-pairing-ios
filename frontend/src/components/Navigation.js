import React from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { Wine, Utensils, MessageCircle, Home, BookOpen, Users, Grape, Heart, Compass, Database } from 'lucide-react';
import { useLanguage } from "@/contexts/LanguageContext";

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useLanguage();

  // Main nav items (shown on mobile dock - scrollable)
  const mainNavItems = [
    { path: '/', icon: Home, labelKey: 'nav_home' },
    { path: '/pairing', icon: Utensils, labelKey: 'nav_pairing' },
    { path: '/sommelier-kompass', icon: Compass, labelKey: 'regional_nav' },
    { path: '/grapes', icon: Grape, labelKey: 'nav_grapes' },
    { path: '/wine-database', icon: Database, labelKey: 'nav_wine_database' },
    { path: '/favorites', icon: Heart, labelKey: 'nav_favorites' },
    { path: '/feed', icon: Users, labelKey: 'nav_feed' },
    { path: '/chat', icon: MessageCircle, labelKey: 'nav_sommelier', isClaude: true },
  ];

  // Secondary nav items (visible on larger screens)
  const secondaryNavItems = [
    { path: '/cellar', icon: Wine, labelKey: 'nav_cellar' },
    { path: '/blog', icon: BookOpen, labelKey: 'nav_blog' },
  ];

  const allNavItems = [...mainNavItems.slice(0, 6), ...secondaryNavItems, mainNavItems[6]];

  return (
    <nav className="nav-dock fixed bottom-0 left-0 right-0 md:left-1/2 md:right-auto md:-translate-x-1/2 md:bottom-6 md:rounded-full rounded-t-2xl px-2 md:px-6 py-2 md:py-3 shadow-2xl z-[9999] md:max-w-none" data-testid="main-navigation">
      {/* Mobile: horizontal scroll, Desktop: all visible */}
      <div className="flex items-center gap-0.5 md:gap-2 overflow-x-auto scrollbar-hide">
        {/* Mobile view: show main 5 items */}
        <div className="flex md:hidden items-center gap-0.5">
          {mainNavItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              data-testid={`nav-${item.labelKey.split('_')[1]}`}
              className={`flex items-center justify-center min-w-[44px] h-[44px] rounded-full transition-elegant flex-shrink-0 ${
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
            </button>
          ))}
        </div>

        {/* Desktop view: show all items */}
        <div className="hidden md:flex items-center gap-2">
          {allNavItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              data-testid={`nav-${item.labelKey.split('_')[1]}`}
              className={`flex items-center gap-2 px-4 py-2 rounded-full transition-elegant ${
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
              <span className="text-sm font-medium">{t(item.labelKey)}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
