import React from 'react';
import { Share2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import ShareButtons from './ShareButtons';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

/**
 * SharePairingButton Component
 * 
 * A special share button for wine pairings that generates a nice shareable message.
 * 
 * @param {string} dish - The dish name
 * @param {string} wine - The recommended wine
 * @param {string} wineType - Type of wine (Rotwein, Weißwein, etc.)
 * @param {string} reason - Why this pairing works (optional)
 */
const SharePairingButton = ({ 
  dish, 
  wine, 
  wineType = 'Wein',
  reason = ''
}) => {
  const baseUrl = 'https://wine-pairing.online';
  
  // Create shareable title and description
  const shareTitle = `🍷 ${wineType} zu ${dish}`;
  const shareDescription = wine 
    ? `Meine Wein-Empfehlung: ${wine} passt perfekt zu ${dish}! ${reason ? `Warum? ${reason}` : ''} Entdecke mehr auf wine-pairing.online`
    : `Entdecke den perfekten Wein zu ${dish} auf wine-pairing.online`;
  
  // Create URL with dish parameter for deep linking
  const shareUrl = `${baseUrl}/pairing?dish=${encodeURIComponent(dish)}`;
  
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button 
          variant="outline" 
          size="sm" 
          className="gap-2 text-wine-600 border-wine-200 hover:bg-wine-50 hover:border-wine-300"
        >
          <Share2 size={16} />
          Teilen
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <span className="text-2xl">🍷</span>
            Pairing teilen
          </DialogTitle>
          <DialogDescription>
            Teile deine Wein-Empfehlung mit Freunden!
          </DialogDescription>
        </DialogHeader>
        
        {/* Preview Card */}
        <div className="bg-gradient-to-br from-wine-50 to-amber-50 rounded-lg p-4 my-4 border border-wine-100">
          <p className="font-semibold text-wine-800 mb-1">{shareTitle}</p>
          {wine && (
            <p className="text-sm text-wine-600 mb-2">
              Empfehlung: <span className="font-medium">{wine}</span>
            </p>
          )}
          {reason && (
            <p className="text-xs text-gray-600 italic">"{reason}"</p>
          )}
        </div>
        
        {/* Share Buttons */}
        <div className="flex justify-center">
          <ShareButtons 
            url={shareUrl}
            title={shareTitle}
            description={shareDescription}
            hashtags="WeinPairing,Wein,Foodpairing,Sommelier"
            size="md"
          />
        </div>
        
        <p className="text-xs text-center text-gray-500 mt-4">
          Tipp: Auf Instagram & TikTok wird der Link kopiert, den du in deiner Story oder Bio einfügen kannst.
        </p>
      </DialogContent>
    </Dialog>
  );
};

export default SharePairingButton;
