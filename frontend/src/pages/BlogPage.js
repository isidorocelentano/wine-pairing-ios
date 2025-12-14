import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Wine, ArrowRight, Calendar, User, Tag, Loader2, Search, X } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useLanguage } from '@/contexts/LanguageContext';
import { SEO } from '@/components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BlogPage = () => {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const fetchCategories = useCallback(async () => {
    try {
      const response = await axios.get(`${API}/blog-categories`);
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  }, []);

  const fetchPosts = useCallback(async () => {
    try {
      const params = selectedCategory ? `?category=${selectedCategory}` : '';
      const response = await axios.get(`${API}/blog${params}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory]);

  // Volltextsuche über Backend-API
  const searchPosts = useCallback(async (query) => {
    if (!query.trim() || query.length < 2) {
      setIsSearching(false);
      return;
    }
    
    setIsSearching(true);
    try {
      const response = await axios.get(`${API}/blog-search?q=${encodeURIComponent(query)}`);
      setPosts(response.data);
    } catch (error) {
      console.error('Search error:', error);
      setPosts([]);
    }
  }, []);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery && searchQuery.length >= 2) {
        searchPosts(searchQuery);
      } else if (isSearching && !searchQuery) {
        setIsSearching(false);
        fetchPosts();
      }
    }, 300);
    
    return () => clearTimeout(timer);
  }, [searchQuery, searchPosts, isSearching, fetchPosts]);

  useEffect(() => {
    fetchPosts();
    fetchCategories();
  }, [fetchPosts, fetchCategories]);

  const getLocalizedTitle = (post) => {
    if (language === 'en' && post.title_en) return post.title_en;
    if (language === 'fr' && post.title_fr) return post.title_fr;
    return post.title;
  };

  const getLocalizedExcerpt = (post) => {
    if (language === 'en' && post.excerpt_en) return post.excerpt_en;
    if (language === 'fr' && post.excerpt_fr) return post.excerpt_fr;
    return post.excerpt;
  };

  const getCategoryLabel = (cat) => {
    const labels = {
      tipps: t('blog_cat_tipps'),
      wissen: t('blog_cat_wissen'),
      pairings: t('blog_cat_pairings'),
      regionen: t('blog_cat_regionen')
    };
    return labels[cat] || cat;
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString(language === 'de' ? 'de-DE' : language === 'fr' ? 'fr-FR' : 'en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <>
      <SEO 
        title={t('blog_title')}
        description={t('blog_description')}
        url="https://wine-pairing.online/blog"
      />
      
      <div className="min-h-screen pb-20 md:pb-24 pt-6 md:pt-8 px-4 md:px-12 lg:px-24" data-testid="blog-page">
        <div className="container mx-auto max-w-6xl">
          <header className="text-center mb-8 md:mb-12">
            <p className="text-accent font-accent text-sm tracking-widest uppercase mb-2">{t('blog_tagline')}</p>
            <h1 className="text-2xl md:text-4xl font-semibold tracking-tight mb-3 md:mb-4">{t('blog_title')}</h1>
            <p className="text-muted-foreground max-w-xl mx-auto text-sm md:text-base">
              {t('blog_description')}
            </p>
          </header>

          {/* Suchfeld */}
          <div className="max-w-xl mx-auto mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder={language === 'de' ? 'Suche nach Weinregionen, Rebsorten, Tipps...' : 
                            language === 'fr' ? 'Rechercher des régions viticoles, cépages, conseils...' :
                            'Search wine regions, grape varieties, tips...'}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-10 py-5 bg-background/80 backdrop-blur-sm border-border/50 rounded-full text-sm"
                data-testid="blog-search"
              />
              {searchQuery && (
                <button
                  onClick={() => {
                    setSearchQuery('');
                    setIsSearching(false);
                    fetchPosts();
                  }}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-accent rounded-full transition-colors"
                >
                  <X className="h-4 w-4 text-muted-foreground" />
                </button>
              )}
            </div>
            {isSearching && (
              <p className="text-center text-sm text-muted-foreground mt-2">
                {posts.length} {language === 'de' ? 'Ergebnisse für' : language === 'fr' ? 'résultats pour' : 'results for'} &ldquo;{searchQuery}&rdquo;
              </p>
            )}
          </div>

          {/* Categories */}
          <div className="flex flex-wrap gap-2 justify-center mb-8">
            <Button
              variant={selectedCategory === null && !isSearching ? 'default' : 'outline'}
              size="sm"
              className="rounded-full"
              onClick={() => {
                setSelectedCategory(null);
                setSearchQuery('');
                setIsSearching(false);
              }}
              data-testid="category-all"
            >
              {t('blog_all')}
            </Button>
            {categories.map((cat) => (
              <Button
                key={cat.category}
                variant={selectedCategory === cat.category && !isSearching ? 'default' : 'outline'}
                size="sm"
                className="rounded-full"
                onClick={() => {
                  setSelectedCategory(cat.category);
                  setSearchQuery('');
                  setIsSearching(false);
                }}
                data-testid={`category-${cat.category}`}
              >
                {getCategoryLabel(cat.category)} ({cat.count})
              </Button>
            ))}
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : posts.length === 0 ? (
            <Card className="bg-secondary/30 border-dashed border-2 border-border">
              <CardContent className="py-16 text-center">
                {isSearching ? (
                  <>
                    <Search className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                    <h3 className="text-xl font-medium mb-2">
                      {language === 'de' ? 'Keine Ergebnisse gefunden' : 
                       language === 'fr' ? 'Aucun résultat trouvé' : 
                       'No results found'}
                    </h3>
                    <p className="text-muted-foreground text-sm mb-4">
                      {language === 'de' ? `Keine Artikel für "${searchQuery}" gefunden.` :
                       language === 'fr' ? `Aucun article trouvé pour "${searchQuery}".` :
                       `No articles found for "${searchQuery}".`}
                    </p>
                    <Button 
                      variant="outline" 
                      onClick={() => {
                        setSearchQuery('');
                        setIsSearching(false);
                        fetchPosts();
                      }}
                    >
                      {language === 'de' ? 'Suche zurücksetzen' : 
                       language === 'fr' ? 'Réinitialiser la recherche' : 
                       'Reset search'}
                    </Button>
                  </>
                ) : (
                  <>
                    <Wine className="h-16 w-16 mx-auto mb-4 text-muted-foreground" strokeWidth={1} />
                    <h3 className="text-xl font-medium mb-2">
                      {language === 'de' ? 'Keine Artikel gefunden' : 
                       language === 'fr' ? 'Aucun article trouvé' : 
                       'No articles found'}
                    </h3>
                  </>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {posts.map((post, idx) => (
                <article key={post.id} data-testid="blog-card">
                  <Card 
                    className="h-full bg-card/50 backdrop-blur-sm border-border/50 hover-lift cursor-pointer overflow-hidden group"
                    onClick={() => navigate(`/blog/${post.slug}`)}
                  >
                    {post.image_url && (
                      <div className="aspect-[16/10] overflow-hidden">
                        <img 
                          src={post.image_url} 
                          alt={getLocalizedTitle(post)}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                          loading="lazy"
                        />
                      </div>
                    )}
                    <CardHeader className="pb-2">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline" className="text-xs">
                          {getCategoryLabel(post.category)}
                        </Badge>
                      </div>
                      <CardTitle className="text-lg md:text-xl leading-tight group-hover:text-primary transition-colors">
                        {getLocalizedTitle(post)}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground text-sm line-clamp-3 mb-4">
                        {getLocalizedExcerpt(post)}
                      </p>
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          <span>{formatDate(post.created_at)}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <User className="w-3 h-3" />
                          <span>{post.author}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 mt-4 text-primary text-sm font-medium group-hover:gap-2 transition-all">
                        {t('blog_read_more')} <ArrowRight className="w-4 h-4" />
                      </div>
                    </CardContent>
                  </Card>
                </article>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default BlogPage;
