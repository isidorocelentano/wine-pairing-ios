import React from 'react';
import { Mic, MicOff } from 'lucide-react';
import { useLanguage } from "@/contexts/LanguageContext";
import { useVoiceInput } from "@/hooks/useVoiceInput";

const VoiceInputButton = ({ onResult, className = '' }) => {
  const { language, t } = useLanguage();
  const { isListening, isSupported, toggleListening } = useVoiceInput(onResult, language);

  if (!isSupported) return null;

  return (
    <button
      onClick={toggleListening}
      className={`p-3 rounded-full transition-all ${isListening 
        ? 'bg-primary text-primary-foreground animate-pulse' 
        : 'bg-secondary hover:bg-secondary/80'
      } ${className}`}
      data-testid="voice-input-btn"
      title={isListening ? t('listening') : t('chat_voice_hint')}
    >
      {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
    </button>
  );
};

export default VoiceInputButton;
