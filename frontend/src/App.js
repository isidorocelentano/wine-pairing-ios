import React from 'react';
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from 'sonner';
import { HelmetProvider } from 'react-helmet-async';
import { LanguageProvider } from "@/contexts/LanguageContext";
import { DarkModeProvider } from "@/contexts/DarkModeContext";
import { SEO } from "@/components/SEO";
import { OrganizationSchema, WebSiteSchema, SommelierServiceSchema } from "@/components/SEOSchemas";

// Layout Components
import LanguageSelector from "@/components/LanguageSelector";
import Navigation from "@/components/Navigation";

// Pages
import HomePage from "@/pages/HomePage";
import PairingPage from "@/pages/PairingPage";
import CellarPage from "@/pages/CellarPage";
import ChatPage from "@/pages/ChatPage";
import BlogPage from "@/pages/BlogPage";
import BlogPostPage from "@/pages/BlogPostPage";
import FeedPage from "@/pages/FeedPage";
import { GrapesPage, GrapeDetailPage } from "@/pages/GrapesPage";
import WineDatabasePage from "@/pages/WineDatabasePage";
import FavoritesPage from "@/pages/FavoritesPage";
import GrapeAdminPage from "@/pages/GrapeAdminPage";
import DishAdminPage from "@/pages/DishAdminPage";
import PairingSeoPage from "@/pages/PairingSeoPage";
import SeoPairingExplorerPage from "@/pages/SeoPairingExplorerPage";
import DynamicPairingPage from "@/pages/DynamicPairingPage";
import SommelierKompassPage from "@/pages/SommelierKompassPage";
import KontaktPage from "@/pages/KontaktPage";
import ImpressumPage from "@/pages/ImpressumPage";
import DatenschutzPage from "@/pages/DatenschutzPage";

function App() {
  return (
    <HelmetProvider>
      <DarkModeProvider>
        <LanguageProvider>
          <div className="App" data-testid="wine-pairing-app">
            {/* Global SEO Schemas */}
            <OrganizationSchema />
            <WebSiteSchema />
            <SommelierServiceSchema />
            
            <Toaster position="top-center" richColors />
            <BrowserRouter>
              <LanguageSelector />
              <Routes>
                <Route path="/" element={<><SEO /><HomePage /><Navigation /></>} />
                <Route path="/pairing" element={<><PairingPage /><Navigation /></>} />
                <Route path="/pairing/:slug" element={<><PairingSeoPage /><Navigation /></>} />
                <Route path="/grapes" element={<><GrapesPage /><Navigation /></>} />
                <Route path="/grapes/:slug" element={<><GrapeDetailPage /><Navigation /></>} />
                <Route path="/wine-database" element={<><WineDatabasePage /><Navigation /></>} />
                <Route path="/favorites" element={<><FavoritesPage /><Navigation /></>} />
                <Route path="/cellar" element={<><CellarPage /><Navigation /></>} />
                <Route path="/admin/grapes" element={<><GrapeAdminPage /><Navigation /></>} />
                <Route path="/admin/dishes" element={<><DishAdminPage /><Navigation /></>} />
                <Route path="/seo/pairings" element={<><SeoPairingExplorerPage /><Navigation /></>} />
                <Route path="/feed" element={<><FeedPage /><Navigation /></>} />
                <Route path="/sommelier-kompass" element={<><SommelierKompassPage /><Navigation /></>} />
                <Route path="/chat" element={<><ChatPage /><Navigation /></>} />
                <Route path="/blog" element={<><BlogPage /><Navigation /></>} />
                <Route path="/blog/:slug" element={<><BlogPostPage /><Navigation /></>} />
                <Route path="/kontakt" element={<><KontaktPage /><Navigation /></>} />
                <Route path="/impressum" element={<><ImpressumPage /><Navigation /></>} />
                <Route path="/datenschutz" element={<><DatenschutzPage /><Navigation /></>} />
              </Routes>
            </BrowserRouter>
          </div>
        </LanguageProvider>
      </DarkModeProvider>
    </HelmetProvider>
  );
}

export default App;
