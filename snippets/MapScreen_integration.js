// ═══════════════════════════════════════════════════════════════
// GUIDE: What to add to idrms_MobApp/src/screens/MapScreen.js
// Do this AFTER FastAPI is running with ngrok!
// ═══════════════════════════════════════════════════════════════

// ── STEP 1 ──────────────────────────────────────────────────────
// Add this at the very TOP of MapScreen.js (before export default)
// Replace with your own ngrok URL after running: ngrok http 8001

const FASTAPI_URL = "https://YOUR-OWN-NGROK-URL.ngrok-free.app"

// ── STEP 2 ──────────────────────────────────────────────────────
// Inside mapHTML, find this line:
//   render();
// Add this RIGHT AFTER render():

/*
fetch(`${FASTAPI_URL}/ai/flood/heatmap`, {
  headers: { 'ngrok-skip-browser-warning': 'true' }
})
  .then(r => r.json())
  .then(data => {
    const colors = {
      High:   '#e84855',
      Medium: '#f4a35a',
      Low:    '#00d68f'
    };
    (data.heatmap || []).forEach(p => {
      const color = colors[p.risk_level] || '#5bc0eb';
      L.circle([p.lat, p.lng], {
        radius:      130,
        color:       color,
        fillColor:   color,
        fillOpacity: p.weight * 0.30,
        weight:      2.5,
        dashArray:   '6 4',
      }).addTo(map).bindPopup(
        '<b>' + p.zone + '</b><br>' +
        '<span style="color:' + color + ';font-weight:800">' +
        p.risk_level + ' Flood Risk</span><br>' +
        '🌊 Flood Incidents: <b>' + p.flood_count + '</b><br>' +
        '📊 AI Score: <b>' + p.ai_score + '</b>/100'
      );
    });
  })
  .catch(() => console.log('FastAPI offline — heatmap skipped'));
*/