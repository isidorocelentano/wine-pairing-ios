import React, { useState } from 'react';
import { 
  Facebook, 
  Linkedin, 
  Twitter, 
  Link2, 
  Check,
  Share2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

/**
 * ShareButtons Component
 * 
 * Displays social media share buttons for sharing content.
 * 
 * @param {string} url - The URL to share (defaults to current page)
 * @param {string} title - The title/text to share
 * @param {string} description - Optional description for platforms that support it
 * @param {string} hashtags - Comma-separated hashtags (without #)
 * @param {string} variant - 'buttons' (individual buttons) or 'dropdown' (single button with menu)
 * @param {string} size - 'sm', 'md', 'lg'
 */
const ShareButtons = ({ 
  url, 
  title, 
  description = '',
  hashtags = 'WeinPairing,Wein,Sommelier',
  variant = 'buttons',
  size = 'md'
}) => {
  const [copied, setCopied] = useState(false);
  
  // Use current URL if not provided
  const shareUrl = url || (typeof window !== 'undefined' ? window.location.href : '');
  const shareTitle = title || 'Entdecke wine-pairing.online - Dein KI-Sommelier';
  const shareDescription = description || 'Finde den perfekten Wein zu jedem Gericht mit KI-Unterstützung!';
  
  // Encode for URLs
  const encodedUrl = encodeURIComponent(shareUrl);
  const encodedTitle = encodeURIComponent(shareTitle);
  const encodedDescription = encodeURIComponent(shareDescription);
  const encodedHashtags = encodeURIComponent(hashtags);
  
  // Share URLs for each platform
  const shareLinks = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedTitle}`,
    twitter: `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}&hashtags=${encodedHashtags}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
    // TikTok doesn't have a direct share URL, but we can copy the link
    // Instagram also doesn't support direct web sharing
  };
  
  // Open share popup
  const openShareWindow = (platform) => {
    const url = shareLinks[platform];
    if (url) {
      window.open(url, '_blank', 'width=600,height=400,scrollbars=yes');
    }
  };
  
  // Copy link to clipboard
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      toast.success('Link kopiert!');
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Kopieren fehlgeschlagen');
    }
  };
  
  // Native share (for mobile)
  const nativeShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: shareTitle,
          text: shareDescription,
          url: shareUrl,
        });
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err);
        }
      }
    } else {
      copyToClipboard();
    }
  };
  
  // Size classes
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12'
  };
  
  const iconSizes = {
    sm: 16,
    md: 20,
    lg: 24
  };
  
  // TikTok Icon (custom SVG)
  const TikTokIcon = ({ size = 20 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-1-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z"/>
    </svg>
  );
  
  // Instagram Icon (custom SVG since lucide doesn't have it)
  const InstagramIcon = ({ size = 20 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
    </svg>
  );

  // Dropdown variant
  if (variant === 'dropdown') {
    return (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="icon" className={sizeClasses[size]}>
            <Share2 size={iconSizes[size]} />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem onClick={() => openShareWindow('facebook')} className="cursor-pointer">
            <Facebook className="mr-2 h-4 w-4 text-blue-600" />
            Facebook
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => openShareWindow('twitter')} className="cursor-pointer">
            <Twitter className="mr-2 h-4 w-4 text-sky-500" />
            X / Twitter
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => openShareWindow('linkedin')} className="cursor-pointer">
            <Linkedin className="mr-2 h-4 w-4 text-blue-700" />
            LinkedIn
          </DropdownMenuItem>
          <DropdownMenuItem onClick={nativeShare} className="cursor-pointer">
            <InstagramIcon size={16} />
            <span className="ml-2">Instagram</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={nativeShare} className="cursor-pointer">
            <TikTokIcon size={16} />
            <span className="ml-2">TikTok</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={copyToClipboard} className="cursor-pointer">
            {copied ? (
              <Check className="mr-2 h-4 w-4 text-green-600" />
            ) : (
              <Link2 className="mr-2 h-4 w-4" />
            )}
            {copied ? 'Kopiert!' : 'Link kopieren'}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    );
  }

  // Buttons variant (default)
  return (
    <div className="flex items-center gap-2 flex-wrap">
      {/* Facebook */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300`}
        onClick={() => openShareWindow('facebook')}
        title="Auf Facebook teilen"
      >
        <Facebook size={iconSizes[size]} />
      </Button>
      
      {/* X / Twitter */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} hover:bg-sky-50 hover:text-sky-500 hover:border-sky-300`}
        onClick={() => openShareWindow('twitter')}
        title="Auf X teilen"
      >
        <Twitter size={iconSizes[size]} />
      </Button>
      
      {/* LinkedIn */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} hover:bg-blue-50 hover:text-blue-700 hover:border-blue-400`}
        onClick={() => openShareWindow('linkedin')}
        title="Auf LinkedIn teilen"
      >
        <Linkedin size={iconSizes[size]} />
      </Button>
      
      {/* Instagram (opens native share or copies link) */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} hover:bg-pink-50 hover:text-pink-600 hover:border-pink-300`}
        onClick={nativeShare}
        title="Für Instagram teilen"
      >
        <InstagramIcon size={iconSizes[size]} />
      </Button>
      
      {/* TikTok (opens native share or copies link) */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} hover:bg-gray-100 hover:border-gray-400`}
        onClick={nativeShare}
        title="Für TikTok teilen"
      >
        <TikTokIcon size={iconSizes[size]} />
      </Button>
      
      {/* Copy Link */}
      <Button
        variant="outline"
        size="icon"
        className={`${sizeClasses[size]} ${copied ? 'bg-green-50 text-green-600 border-green-300' : 'hover:bg-gray-100'}`}
        onClick={copyToClipboard}
        title="Link kopieren"
      >
        {copied ? <Check size={iconSizes[size]} /> : <Link2 size={iconSizes[size]} />}
      </Button>
    </div>
  );
};

export default ShareButtons;
