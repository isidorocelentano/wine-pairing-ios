import React from 'react';
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from 'sonner';
import { HelmetProvider } from 'react-helmet-async';
import { LanguageProvider } from "@/contexts/LanguageContext";
import { DarkModeProvider } from "@/contexts/DarkModeContext";
import { AuthProvider } from "@/contexts/AuthContext";
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
import PairingSciencePage from "@/pages/PairingSciencePage";
import SommelierKompassPage from "@/pages/SommelierKompassPage";
import KontaktPage from "@/pages/KontaktPage";
import ImpressumPage from "@/pages/ImpressumPage";
import DatenschutzPage from "@/pages/DatenschutzPage";
import LoginPage from "@/pages/LoginPage";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage";
import ResetPasswordPage from "@/pages/ResetPasswordPage";
import SubscriptionPage from "@/pages/SubscriptionPage";
import SubscriptionSuccessPage from "@/pages/SubscriptionSuccessPage";
import CouponPage from "@/pages/CouponPage";
import PricingPage from "@/pages/PricingPage";

function App() {
  return (
    <HelmetProvider>
      <DarkModeProvider>
        <LanguageProvider>
          <AuthProvider>
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
                  <Route path="/pairing/:slug" element={<><DynamicPairingPage /><Navigation /></>} />
                  <Route path="/grapes" element={<><GrapesPage /><Navigation /></>} />
                  <Route path="/grapes/:slug" element={<><GrapeDetailPage /><Navigation /></>} />
                  <Route path="/wine-database" element={<><WineDatabasePage /><Navigation /></>} />
                  <Route path="/favorites" element={<><FavoritesPage /><Navigation /></>} />
                  <Route path="/cellar" element={<><CellarPage /><Navigation /></>} />
                  <Route path="/weinkeller" element={<><CellarPage /><Navigation /></>} />
                  <Route path="/admin/grapes" element={<><GrapeAdminPage /><Navigation /></>} />
                  <Route path="/admin/dishes" element={<><DishAdminPage /><Navigation /></>} />
                  <Route path="/seo/pairings" element={<><SeoPairingExplorerPage /><Navigation /></>} />
                  <Route path="/feed" element={<><FeedPage /><Navigation /></>} />
                  <Route path="/sommelier-kompass" element={<><SommelierKompassPage /><Navigation /></>} />
                  <Route path="/pairing-science" element={<><PairingSciencePage /><Navigation /></>} />
                  <Route path="/wie-wir-pairen" element={<><PairingSciencePage /><Navigation /></>} />
                  <Route path="/chat" element={<><ChatPage /><Navigation /></>} />
                  <Route path="/blog" element={<><BlogPage /><Navigation /></>} />
                  <Route path="/blog/:slug" element={<><BlogPostPage /><Navigation /></>} />
                  <Route path="/kontakt" element={<><KontaktPage /><Navigation /></>} />
                  <Route path="/impressum" element={<><ImpressumPage /><Navigation /></>} />
                  <Route path="/datenschutz" element={<><DatenschutzPage /><Navigation /></>} />
                  {/* Auth & Subscription Routes */}
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                  <Route path="/reset-password" element={<ResetPasswordPage />} />
                  <Route path="/subscription" element={<><SubscriptionPage /><Navigation /></>} />
                  <Route path="/subscription/success" element={<SubscriptionSuccessPage />} />
                  <Route path="/subscription/cancel" element={<><SubscriptionPage /><Navigation /></>} />
                  <Route path="/coupon" element={<><CouponPage /><Navigation /></>} />
                  <Route path="/pricing" element={<><PricingPage /><Navigation /></>} />
                  <Route path="/pro" element={<><PricingPage /><Navigation /></>} />
                </Routes>
              </BrowserRouter>
            </div>
          </AuthProvider>
        </LanguageProvider>
      </DarkModeProvider>
    </HelmetProvider>
  );
}

export default App;
