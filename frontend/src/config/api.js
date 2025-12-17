/**
 * API Configuration
 * 
 * Dynamische Backend-URL basierend auf dem aktuellen Host.
 * Dies stellt sicher, dass die App sowohl in der Preview als auch auf Custom Domains funktioniert.
 */

// Bestimme die Backend-URL basierend auf dem aktuellen Host
const getBackendUrl = () => {
  // Wenn REACT_APP_BACKEND_URL gesetzt ist und wir auf derselben Domain sind, verwende sie
  const envUrl = process.env.REACT_APP_BACKEND_URL;
  
  // Im Browser: Prüfe ob wir auf einer Custom Domain sind
  if (typeof window !== 'undefined') {
    const currentHost = window.location.origin;
    
    // Wenn wir auf wine-pairing.online sind, verwende dieselbe Domain für API
    if (currentHost.includes('wine-pairing.online')) {
      return 'https://wine-pairing.online';
    }
    
    // Wenn wir auf einer .emergent.host oder .emergentagent.com Domain sind
    if (currentHost.includes('.emergent')) {
      // Verwende die Umgebungsvariable oder die aktuelle Domain
      return envUrl || currentHost;
    }
    
    // Für localhost Development
    if (currentHost.includes('localhost')) {
      return envUrl || 'http://localhost:8001';
    }
  }
  
  // Fallback auf Umgebungsvariable
  return envUrl || '';
};

export const API_URL = getBackendUrl();
export const API = `${API_URL}/api`;

// Debug-Logging (nur in Development)
if (process.env.NODE_ENV === 'development') {
  console.log('API Configuration:', { API_URL, API });
}
