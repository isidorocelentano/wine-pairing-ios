/**
 * API Configuration
 * 
 * Dynamische Backend-URL basierend auf dem aktuellen Host.
 * Dies stellt sicher, dass die App sowohl in der Preview als auch auf Custom Domains funktioniert.
 * 
 * WICHTIG: Für Produktion verwendet window.location.origin für maximale Flexibilität.
 * Für localhost Entwicklung verwendet Port 8001.
 */

// Bestimme die Backend-URL basierend auf dem aktuellen Host
const getBackendUrl = () => {
  // Im Browser: Dynamische URL basierend auf Host
  if (typeof window !== 'undefined') {
    const origin = window.location.origin;
    
    // Localhost Development: Backend läuft auf Port 8001
    if (origin.includes('localhost:3000')) {
      return 'http://localhost:8001';
    }
    
    // Produktion/Preview: Gleiche Domain für Frontend und Backend
    return origin;
  }
  
  // Server-side oder Build-Zeit: Verwende Umgebungsvariable
  return process.env.REACT_APP_BACKEND_URL || '';
};

export const API_URL = getBackendUrl();
export const API = `${API_URL}/api`;

// Debug-Logging (nur in Development)
if (process.env.NODE_ENV === 'development') {
  console.log('API Configuration:', { API_URL, API });
}
