import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from "axios";
import { toast } from 'sonner';
import { Wine, Camera, X, Send, Loader2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useLanguage } from "@/contexts/LanguageContext";
import VoiceInputButton from "@/components/VoiceInputButton";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ChatPage = () => {
  const { t, language } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [imageBase64, setImageBase64] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleVoiceResult = useCallback((transcript) => {
    setInput(prev => prev + (prev ? ' ' : '') + transcript);
  }, []);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => { scrollToBottom(); }, [messages]);

  const handleSend = async () => {
    if (!input.trim() && !imageBase64) return;

    const userMessage = { role: 'user', content: input, image: imageBase64 };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        message: input || 'Was siehst du auf diesem Bild?',
        session_id: sessionId,
        image_base64: imageBase64,
        language: language
      });

      setSessionId(response.data.session_id);
      setMessages((prev) => [...prev, { role: 'assistant', content: response.data.response }]);
      setImageBase64(null);
    } catch (error) {
      toast.error(t('error_general'));
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImageBase64(reader.result.split(',')[1]);
      reader.readAsDataURL(file);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestions = [t('chat_suggestion1'), t('chat_suggestion2'), t('chat_suggestion3')];

  return (
    <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="chat-page">
      <div className="container mx-auto max-w-3xl h-[calc(100vh-140px)] md:h-[calc(100vh-180px)] flex flex-col">
        <header className="mb-4 md:mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 md:gap-6">
            <div className="text-center md:text-left">
              <div className="sommelier-avatar w-14 md:w-20 h-14 md:h-20 rounded-full mx-auto md:mx-0 mb-3 md:mb-4 overflow-hidden border border-border/60 shadow-md">
                <img
                  src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/w9w52bm4_CLAUDE%20SOMMELIER%2001%20%284%29.png"
                  alt="Claude, virtueller Sommelier"
                  className="w-full h-full object-cover"
                />
              </div>
              <h1 className="text-xl md:text-3xl font-semibold tracking-tight">{t('chat_title')}</h1>
              <p className="text-muted-foreground text-xs md:text-sm mt-1 md:mt-2">{t('chat_subtitle')}</p>
            </div>
            <div className="hidden md:block w-40 lg:w-56 rounded-2xl overflow-hidden shadow-xl border border-border/60">
              <img
                src="https://customer-assets.emergentagent.com/job_e57eae36-225b-4e20-a944-048ef9749606/artifacts/ulsy1h5x_CLAUDE%20SOMMELIER%2001%20%286%29.png"
                alt="Claude im Weinkeller"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          <div className="mt-3 md:mt-4 p-3 md:p-4 rounded-xl bg-muted/40 border border-border/40 text-left">
            <h2 className="text-sm md:text-base font-semibold mb-1">{t('claude_bio_title')}</h2>
            <p className="text-[11px] md:text-sm text-muted-foreground leading-snug">
              {t('claude_bio_text1')}
            </p>
            <p className="hidden md:block text-[11px] md:text-sm text-muted-foreground leading-snug mt-1">
              {t('claude_bio_text2')}
            </p>
          </div>
        </header>

        <Card className="flex-1 bg-card/50 backdrop-blur-sm border-border/50 flex flex-col overflow-hidden">
          <ScrollArea className="flex-1 p-3 md:p-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center py-8 md:py-12">
                <Wine className="h-10 md:h-12 w-10 md:w-12 text-muted-foreground/30 mb-4" strokeWidth={1} />
                <p className="text-muted-foreground text-sm md:text-base">{t('chat_empty')}</p>
                <div className="flex flex-wrap gap-2 mt-4 md:mt-6 justify-center">
                  {suggestions.map((q) => (
                    <button key={q} onClick={() => setInput(q)} className="px-3 md:px-4 py-2 bg-secondary/50 rounded-full text-xs md:text-sm hover:bg-secondary transition-colors">
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-3 md:space-y-4">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] md:max-w-[80%] p-3 md:p-4 ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`} data-testid={`chat-message-${msg.role}`}>
                      {msg.image && <img src={`data:image/jpeg;base64,${msg.image}`} alt="Uploaded" className="max-w-[150px] md:max-w-[200px] rounded mb-2" />}
                      <p className="text-xs md:text-sm whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex justify-start">
                    <div className="chat-bubble-assistant p-3 md:p-4"><Loader2 className="h-4 md:h-5 w-4 md:w-5 animate-spin" /></div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </ScrollArea>

          <div className="p-3 md:p-4 border-t border-border/50">
            {imageBase64 && (
              <div className="mb-3 relative inline-block">
                <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Preview" className="h-12 md:h-16 rounded" />
                <button onClick={() => setImageBase64(null)} className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1">
                  <X className="h-3 w-3" />
                </button>
              </div>
            )}
            <div className="flex gap-2 md:gap-3">
              <button onClick={() => fileInputRef.current?.click()} className="p-2 md:p-3 rounded-full bg-secondary hover:bg-secondary/80 transition-colors" data-testid="chat-upload-btn">
                <Camera className="h-4 md:h-5 w-4 md:w-5" />
              </button>
              <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
              <VoiceInputButton onResult={handleVoiceResult} />
              <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={handleKeyPress} placeholder={t('chat_placeholder')} className="flex-1 rounded-full text-sm" data-testid="chat-input" />
              <Button onClick={handleSend} disabled={loading || (!input.trim() && !imageBase64)} className="rounded-full px-4 md:px-6" data-testid="chat-send-btn">
                <Send className="h-4 md:h-5 w-4 md:w-5" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ChatPage;
