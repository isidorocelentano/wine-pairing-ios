import React from 'react';
import { Globe, Sun, Moon } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useLanguage } from "@/contexts/LanguageContext";
import { useDarkMode } from "@/contexts/DarkModeContext";

const LanguageSelector = () => {
  const { language, setLanguage, languageNames, languages } = useLanguage();
  const { isDark, toggleDarkMode } = useDarkMode();

  return (
    <div className="fixed top-4 right-4 z-50 flex items-center gap-2" data-testid="language-selector">
      {/* Dark Mode Toggle */}
      <Button
        variant="outline"
        size="icon"
        onClick={toggleDarkMode}
        className="rounded-full bg-background/80 backdrop-blur-sm border-border/50 hover:bg-accent"
        aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
      </Button>

      {/* Language Selector */}
      <Select value={language} onValueChange={setLanguage}>
        <SelectTrigger className="w-auto gap-2 bg-background/80 backdrop-blur-sm border-border/50 rounded-full px-4">
          <Globe className="w-4 h-4" />
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {languages.map((lang) => (
            <SelectItem key={lang} value={lang}>
              {languageNames[lang]}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default LanguageSelector;
