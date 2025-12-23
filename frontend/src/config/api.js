/**
 * API Configuration
 * 
 * Dynamische Backend-URL basierend auf dem aktuellen Host.
 * Dies stellt sicher, dass die App sowohl in der Preview als auch auf Custom Domains funktioniert.
 * 
 * WICHTIG: Verwendet window.location.origin für maximale Flexibilität.
 */

// Bestimme die Backend-URL basierend auf dem aktuellen Host
const getBackendUrl = () => {
  // Im Browser: Verwende immer die aktuelle Domain
  if (typeof window !== 'undefined') {
    return window.location.origin;
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
