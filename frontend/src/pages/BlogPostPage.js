import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Calendar, User, Tag, Share2, Facebook, Twitter, Linkedin, Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BlogPostPage = () => {
  const { slug } = useParams();
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [relatedPosts, setRelatedPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPost();
  }, [slug]);

  const fetchPost = async () => {
    try {
      const response = await axios.get(`${API}/blog/${slug}`);
      setPost(response.data);
      
      // Fetch related posts from same category
      const relatedResponse = await axios.get(`${API}/blog?category=${response.data.category}&limit=3`);
      setRelatedPosts(relatedResponse.data.filter(p => p.slug !== slug).slice(0, 2));
    } catch (error) {
      console.error('Error fetching post:', error);
      navigate('/blog');
    } finally {
      setLoading(false);
    }
  };

  const getLocalizedTitle = (p) => {
    if (language === 'en' && p.title_en) return p.title_en;
    if (language === 'fr' && p.title_fr) return p.title_fr;
    return p.title;
  };

  const getLocalizedContent = (p) => {
    if (language === 'en' && p.content_en) return p.content_en;
    if (language === 'fr' && p.content_fr) return p.content_fr;
    return p.content;
  };

  const getLocalizedExcerpt = (p) => {
    if (language === 'en' && p.excerpt_en) return p.excerpt_en;
    if (language === 'fr' && p.excerpt_fr) return p.excerpt_fr;
    return p.excerpt;
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(language === 'de' ? 'de-DE' : language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const shareUrl = `https://wine-pairing.online/blog/${slug}`;

  const handleShare = (platform) => {
    const title = post ? getLocalizedTitle(post) : '';
    const urls = {
      twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(shareUrl)}`,
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`,
      linkedin: `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(title)}`
    };
    window.open(urls[platform], '_blank', 'width=600,height=400');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!post) return null;

  // Convert markdown-like content to HTML
  const renderContent = (content) => {
    return content
      .split('\n')
      .map((line, i) => {
        if (line.startsWith('## ')) {
          return <h2 key={i} className="text-2xl font-semibold mt-8 mb-4">{line.replace('## ', '')}</h2>;
        }
        if (line.startsWith('### ')) {
          return <h3 key={i} className="text-xl font-semibold mt-6 mb-3">{line.replace('### ', '')}</h3>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <p key={i} className="font-semibold mt-4 mb-2">{line.replace(/\*\*/g, '')}</p>;
        }
        if (line.startsWith('- ')) {
          return <li key={i} className="ml-6 mb-1">{line.replace('- ', '')}</li>;
        }
        if (line.trim() === '') {
          return <br key={i} />;
        }
        return <p key={i} className="mb-3 leading-relaxed">{line}</p>;
      });
  };

  return (
    <>
      <SEO 
        title={getLocalizedTitle(post)}
        description={getLocalizedExcerpt(post)}
        image={post.image_url}
        url={shareUrl}
        type="article"
        article={{
          title: getLocalizedTitle(post),
          author: post.author,
          datePublished: post.created_at,
          dateModified: post.updated_at
        }}
      />
      
      <div className="min-h-screen pb-20 md:pb-24" data-testid="blog-post-page">
        {/* Hero Image */}
        {post.image_url && (
          <div className="relative h-[40vh] md:h-[50vh] w-full">
            <img 
              src={post.image_url} 
              alt={getLocalizedTitle(post)}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent" />
          </div>
        )}
        
        <div className="container mx-auto max-w-3xl px-4 md:px-8 -mt-20 relative z-10">
          {/* Back Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/blog')}
            className="mb-6"
            data-testid="back-to-blog"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {t('blog_back')}
          </Button>

          <article className="bg-card/80 backdrop-blur-md rounded-lg border border-border/50 p-6 md:p-10">
            {/* Meta */}
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <Badge variant="outline">{post.category}</Badge>
              <span className="text-sm text-muted-foreground flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                {formatDate(post.created_at)}
              </span>
              <span className="text-sm text-muted-foreground flex items-center gap-1">
                <User className="w-3 h-3" />
                {post.author}
              </span>
            </div>

            {/* Title */}
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-6">
              {getLocalizedTitle(post)}
            </h1>

            {/* Excerpt */}
            <p className="text-lg text-muted-foreground mb-8 font-accent italic">
              {getLocalizedExcerpt(post)}
            </p>

            {/* Content */}
            <div className="prose prose-lg max-w-none text-foreground/90" data-testid="blog-content">
              {renderContent(getLocalizedContent(post))}
            </div>

            {/* Tags */}
            {post.tags && post.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-8 pt-6 border-t border-border/50">
                <Tag className="w-4 h-4 text-muted-foreground" />
                {post.tags.map((tag) => (
                  <Badge key={tag} variant="secondary" className="text-xs">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}

            {/* Share */}
            <div className="flex items-center gap-3 mt-6 pt-6 border-t border-border/50">
              <span className="text-sm font-medium">{t('blog_share')}:</span>
              <button
                onClick={() => handleShare('twitter')}
                className="p-2 rounded-full bg-secondary hover:bg-secondary/80 transition-colors"
                aria-label="Share on Twitter"
              >
                <Twitter className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleShare('facebook')}
                className="p-2 rounded-full bg-secondary hover:bg-secondary/80 transition-colors"
                aria-label="Share on Facebook"
              >
                <Facebook className="w-4 h-4" />
              </button>
              <button
                onClick={() => handleShare('linkedin')}
                className="p-2 rounded-full bg-secondary hover:bg-secondary/80 transition-colors"
                aria-label="Share on LinkedIn"
              >
                <Linkedin className="w-4 h-4" />
              </button>
            </div>
          </article>

          {/* Related Posts */}
          {relatedPosts.length > 0 && (
            <div className="mt-12">
              <h3 className="text-xl font-semibold mb-6">{t('blog_related')}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {relatedPosts.map((relPost) => (
                  <Card 
                    key={relPost.id}
                    className="bg-card/50 backdrop-blur-sm border-border/50 hover-lift cursor-pointer overflow-hidden"
                    onClick={() => navigate(`/blog/${relPost.slug}`)}
                  >
                    {relPost.image_url && (
                      <div className="aspect-[16/9] overflow-hidden">
                        <img 
                          src={relPost.image_url} 
                          alt={getLocalizedTitle(relPost)}
                          className="w-full h-full object-cover"
                          loading="lazy"
                        />
                      </div>
                    )}
                    <CardContent className="p-4">
                      <h4 className="font-medium line-clamp-2">{getLocalizedTitle(relPost)}</h4>
                      <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                        {getLocalizedExcerpt(relPost)}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default BlogPostPage;
