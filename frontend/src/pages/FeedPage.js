import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Wine, Heart, MessageCircle, Send, Plus, Star, Camera, X, Loader2, Users, TrendingUp, Trash2, Share2, Facebook, Instagram, Copy, Check } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ScrollArea } from '@/components/ui/scroll-area';
import { toast } from 'sonner';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';

import { API_URL as BACKEND_URL, API } from '@/config/api';

// Generate or get user ID from localStorage
const getUserId = () => {
  let userId = localStorage.getItem('wine-app-user-id');
  if (!userId) {
    userId = 'user_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('wine-app-user-id', userId);
  }
  return userId;
};

const getUserName = () => {
  return localStorage.getItem('wine-app-user-name') || '';
};

const setUserName = (name) => {
  localStorage.setItem('wine-app-user-name', name);
};

const FeedPage = () => {
  const { t, language } = useLanguage();
  const [posts, setPosts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [userName, setUserNameState] = useState(getUserName());
  const [userId] = useState(getUserId());
  const fileInputRef = useRef(null);
  
  // Helper to get localized content from a post
  const getLocalizedContent = useCallback((post, field) => {
    // Try language-specific field first, fall back to default
    const langField = `${field}_${language}`;
    if (language !== 'de' && post[langField]) {
      return post[langField];
    }
    return post[field] || '';
  }, [language]);
  
  // New post state
  const [newPost, setNewPost] = useState({
    dish: '',
    wine_name: '',
    wine_type: 'rot',
    rating: 5,
    experience: '',
    image_base64: ''
  });
  const [creating, setCreating] = useState(false);
  
  // Comment state
  const [commentInputs, setCommentInputs] = useState({});
  const [expandedComments, setExpandedComments] = useState({});
  
  // Share state
  const [shareMenuOpen, setShareMenuOpen] = useState({});
  const [copiedPostId, setCopiedPostId] = useState(null);

  const fetchPosts = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/feed`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching feed:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/feed-stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, []);

  useEffect(() => {
    fetchPosts();
    fetchStats();
  }, [fetchPosts, fetchStats]);

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewPost({ ...newPost, image_base64: reader.result.split(',')[1] });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCreatePost = async () => {
    if (!userName.trim()) {
      toast.error(t('feed_name_required'));
      return;
    }
    if (!newPost.dish.trim() || !newPost.wine_name.trim()) {
      toast.error(t('feed_fields_required'));
      return;
    }
    
    setCreating(true);
    try {
      setUserName(userName);
      await axios.post(`${API}/feed`, {
        ...newPost,
        author_name: userName,
        author_id: userId
      });
      toast.success(t('feed_post_created'));
      setShowCreateDialog(false);
      setNewPost({ dish: '', wine_name: '', wine_type: 'rot', rating: 5, experience: '', image_base64: '' });
      fetchPosts();
      fetchStats();
    } catch (error) {
      toast.error(t('error_general'));
    } finally {
      setCreating(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      const response = await axios.post(`${API}/feed/${postId}/like?author_id=${userId}`);
      // Update local state
      setPosts(posts.map(post => {
        if (post.id === postId) {
          const likes = response.data.action === 'liked' 
            ? [...post.likes, userId]
            : post.likes.filter(id => id !== userId);
          return { ...post, likes };
        }
        return post;
      }));
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleComment = async (postId) => {
    const content = commentInputs[postId]?.trim();
    if (!content) return;
    if (!userName.trim()) {
      toast.error(t('feed_name_required'));
      return;
    }
    
    try {
      setUserName(userName);
      await axios.post(`${API}/feed/${postId}/comment`, {
        author_name: userName,
        author_id: userId,
        content
      });
      setCommentInputs({ ...commentInputs, [postId]: '' });
      fetchPosts();
    } catch (error) {
      toast.error(t('error_general'));
    }
  };

  const handleDelete = async (postId) => {
    if (!window.confirm(t('feed_confirm_delete'))) return;
    
    try {
      await axios.delete(`${API}/feed/${postId}?author_id=${userId}`);
      toast.success(t('feed_post_deleted'));
      fetchPosts();
      fetchStats();
    } catch (error) {
      toast.error(error.response?.status === 403 ? t('feed_delete_forbidden') : t('error_general'));
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return t('feed_just_now');
    if (diffMins < 60) return `${diffMins} ${t('feed_minutes_ago')}`;
    if (diffHours < 24) return `${diffHours} ${t('feed_hours_ago')}`;
    if (diffDays < 7) return `${diffDays} ${t('feed_days_ago')}`;
    
    return date.toLocaleDateString(language === 'de' ? 'de-DE' : language === 'fr' ? 'fr-FR' : 'en-US');
  };

  const getWineTypeLabel = (type) => {
    const labels = { rot: t('pairing_red'), weiss: t('pairing_white'), rose: t('pairing_rose'), schaumwein: t('pairing_sparkling') };
    return labels[type] || type;
  };

  const getWineTypeBadgeClass = (type) => {
    const classes = { rot: 'badge-rot', weiss: 'badge-weiss', rose: 'badge-rose', schaumwein: 'badge-schaumwein' };
    return classes[type] || 'bg-secondary';
  };

  const renderStars = (rating, interactive = false, onChange = null) => {
    return (
      <div className="flex gap-0.5">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => interactive && onChange && onChange(star)}
            className={`${interactive ? 'cursor-pointer hover:scale-110' : 'cursor-default'} transition-transform`}
            disabled={!interactive}
          >
            <Star
              className={`w-4 h-4 md:w-5 md:h-5 ${star <= rating ? 'fill-accent text-accent' : 'text-muted-foreground/30'}`}
            />
          </button>
        ))}
      </div>
    );
  };

  return (
    <>
      <SEO 
        title={t('feed_title')}
        description={t('feed_description')}
        url="https://wine-pairing.online/feed"
      />
      
      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="feed-page">
        <div className="container mx-auto max-w-4xl">
          <header className="text-center mb-6 md:mb-8">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('feed_tagline')}</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3">{t('feed_title')}</h1>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
              {t('feed_description')}
            </p>
          </header>

          {/* Stats Bar */}
          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardContent className="p-4 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Users className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-2xl font-semibold">{stats.total_users}</p>
                    <p className="text-xs text-muted-foreground">{t('feed_members')}</p>
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardContent className="p-4 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-accent" />
                  </div>
                  <div>
                    <p className="text-2xl font-semibold">{stats.total_posts}</p>
                    <p className="text-xs text-muted-foreground">{t('feed_experiences')}</p>
                  </div>
                </CardContent>
              </Card>
              <Card className="col-span-2 md:col-span-1 bg-card/50 backdrop-blur-sm border-border/50">
                <CardContent className="p-4">
                  <p className="text-xs text-muted-foreground mb-2">{t('feed_top_pairings')}</p>
                  {stats.top_pairings?.slice(0, 2).map((p, i) => (
                    <p key={i} className="text-sm truncate">
                      <span className="text-accent">{p.wine_name}</span> + {p.dish}
                    </p>
                  ))}
                </CardContent>
              </Card>
            </div>
          )}

          {/* User Name Input (if not set) */}
          {!getUserName() && (
            <Card className="bg-secondary/30 border-border/50 mb-6">
              <CardContent className="p-4">
                <p className="text-sm mb-3">{t('feed_set_name')}</p>
                <div className="flex gap-2">
                  <Input
                    value={userName}
                    onChange={(e) => setUserNameState(e.target.value)}
                    placeholder={t('feed_your_name')}
                    className="flex-1"
                    data-testid="username-input"
                  />
                  <Button onClick={() => setUserName(userName)} disabled={!userName.trim()}>
                    {t('feed_save_name')}
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Create Post Button */}
          <div className="flex justify-center mb-6">
            <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
              <DialogTrigger asChild>
                <Button className="rounded-full px-6" data-testid="create-post-btn">
                  <Plus className="mr-2 h-4 w-4" />{t('feed_share_experience')}
                </Button>
              </DialogTrigger>
              <DialogContent className="mx-4 max-w-md max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle>{t('feed_new_post')}</DialogTitle>
                  <DialogDescription>{t('feed_new_post_desc')}</DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <Input
                    placeholder={t('feed_your_name')}
                    value={userName}
                    onChange={(e) => setUserNameState(e.target.value)}
                    data-testid="post-author-input"
                  />
                  <Input
                    placeholder={t('feed_dish_placeholder')}
                    value={newPost.dish}
                    onChange={(e) => setNewPost({ ...newPost, dish: e.target.value })}
                    data-testid="post-dish-input"
                  />
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      placeholder={t('feed_wine_placeholder')}
                      value={newPost.wine_name}
                      onChange={(e) => setNewPost({ ...newPost, wine_name: e.target.value })}
                      data-testid="post-wine-input"
                    />
                    <Select value={newPost.wine_type} onValueChange={(v) => setNewPost({ ...newPost, wine_type: v })}>
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="rot">{t('pairing_red')}</SelectItem>
                        <SelectItem value="weiss">{t('pairing_white')}</SelectItem>
                        <SelectItem value="rose">{t('pairing_rose')}</SelectItem>
                        <SelectItem value="schaumwein">{t('pairing_sparkling')}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <p className="text-sm mb-2">{t('feed_rating')}</p>
                    {renderStars(newPost.rating, true, (r) => setNewPost({ ...newPost, rating: r }))}
                  </div>
                  
                  <Textarea
                    placeholder={t('feed_experience_placeholder')}
                    value={newPost.experience}
                    onChange={(e) => setNewPost({ ...newPost, experience: e.target.value })}
                    className="min-h-[100px]"
                    data-testid="post-experience-input"
                  />
                  
                  {/* Image Upload */}
                  <div 
                    className="upload-zone rounded-lg p-4 text-center cursor-pointer"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    {newPost.image_base64 ? (
                      <div className="relative inline-block">
                        <img src={`data:image/jpeg;base64,${newPost.image_base64}`} alt="Preview" className="max-h-32 mx-auto rounded" />
                        <button
                          onClick={(e) => { e.stopPropagation(); setNewPost({ ...newPost, image_base64: '' }); }}
                          className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ) : (
                      <><Camera className="h-8 w-8 mx-auto mb-2 text-muted-foreground" /><p className="text-sm text-muted-foreground">{t('feed_add_photo')}</p></>
                    )}
                  </div>
                  <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
                  
                  <Button 
                    onClick={handleCreatePost} 
                    disabled={creating || !newPost.dish.trim() || !newPost.wine_name.trim()}
                    className="w-full rounded-full"
                    data-testid="submit-post-btn"
                  >
                    {creating ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <Wine className="h-4 w-4 mr-2" />}
                    {t('feed_publish')}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Feed Posts */}
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : posts.length === 0 ? (
            <Card className="bg-secondary/30 border-dashed border-2 border-border">
              <CardContent className="py-16 text-center">
                <Users className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                <h3 className="text-xl font-medium mb-2">{t('feed_empty_title')}</h3>
                <p className="text-muted-foreground mb-6">{t('feed_empty_desc')}</p>
                <Button onClick={() => setShowCreateDialog(true)} className="rounded-full">
                  <Plus className="mr-2 h-4 w-4" />{t('feed_first_post')}
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6" data-testid="feed-posts">
              {posts.map((post) => (
                <Card key={post.id} className="bg-card/50 backdrop-blur-sm border-border/50 overflow-hidden" data-testid="feed-post">
                  {/* Post Header */}
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary font-medium">
                          {post.author_name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-medium">{post.author_name}</p>
                          <p className="text-xs text-muted-foreground">{formatDate(post.created_at)}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {renderStars(post.rating)}
                        {post.author_id === userId && (
                          <button
                            onClick={() => handleDelete(post.id)}
                            className="p-2 text-muted-foreground hover:text-destructive transition-colors"
                            data-testid="delete-post-btn"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </div>
                  </CardHeader>
                  
                  {/* Post Content */}
                  <CardContent className="space-y-3">
                    {/* Pairing Info */}
                    <div className="bg-secondary/30 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge className={`${getWineTypeBadgeClass(post.wine_type)} border-0 text-xs`}>
                          {getWineTypeLabel(post.wine_type)}
                        </Badge>
                      </div>
                      <p className="font-medium">
                        <span className="text-primary">{post.wine_name}</span>
                        <span className="text-muted-foreground mx-2">+</span>
                        <span>{getLocalizedContent(post, 'dish')}</span>
                      </p>
                    </div>
                    
                    {/* Experience Text */}
                    {(post.experience || post.experience_en || post.experience_fr) && (
                      <p className="text-sm text-foreground/90 leading-relaxed whitespace-pre-line">
                        {getLocalizedContent(post, 'experience')}
                      </p>
                    )}
                    
                    {/* Image */}
                    {post.image_base64 && (
                      <div className="rounded-lg overflow-hidden">
                        <img 
                          src={`data:image/jpeg;base64,${post.image_base64}`} 
                          alt={`${post.dish} + ${post.wine_name}`}
                          className="w-full max-h-80 object-cover"
                        />
                      </div>
                    )}
                    
                    {/* Actions */}
                    <div className="flex items-center gap-4 pt-2 border-t border-border/50">
                      <button
                        onClick={() => handleLike(post.id)}
                        className={`flex items-center gap-1.5 text-sm transition-colors ${
                          post.likes?.includes(userId) ? 'text-primary' : 'text-muted-foreground hover:text-primary'
                        }`}
                        data-testid="like-btn"
                      >
                        <Heart className={`w-5 h-5 ${post.likes?.includes(userId) ? 'fill-current' : ''}`} />
                        <span>{post.likes?.length || 0}</span>
                      </button>
                      <button
                        onClick={() => setExpandedComments({ ...expandedComments, [post.id]: !expandedComments[post.id] })}
                        className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors"
                        data-testid="comments-btn"
                      >
                        <MessageCircle className="w-5 h-5" />
                        <span>{post.comments?.length || 0}</span>
                      </button>
                    </div>
                    
                    {/* Comments Section */}
                    {expandedComments[post.id] && (
                      <div className="pt-3 space-y-3">
                        {post.comments?.length > 0 && (
                          <ScrollArea className="max-h-48">
                            <div className="space-y-2">
                              {post.comments.map((comment) => (
                                <div key={comment.id} className="bg-secondary/30 rounded-lg p-2">
                                  <p className="text-xs font-medium">{comment.author_name}</p>
                                  <p className="text-sm">{comment.content}</p>
                                </div>
                              ))}
                            </div>
                          </ScrollArea>
                        )}
                        
                        <div className="flex gap-2">
                          <Input
                            placeholder={t('feed_write_comment')}
                            value={commentInputs[post.id] || ''}
                            onChange={(e) => setCommentInputs({ ...commentInputs, [post.id]: e.target.value })}
                            onKeyPress={(e) => e.key === 'Enter' && handleComment(post.id)}
                            className="flex-1 text-sm"
                            data-testid="comment-input"
                          />
                          <Button
                            size="sm"
                            onClick={() => handleComment(post.id)}
                            disabled={!commentInputs[post.id]?.trim()}
                            className="rounded-full"
                            data-testid="submit-comment-btn"
                          >
                            <Send className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default FeedPage;
