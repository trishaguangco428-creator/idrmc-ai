// ═══════════════════════════════════════════════════════════════
// GUIDE: What to add to idrms-lab5/src/pages/MapPage.jsx
// Do this AFTER FastAPI is running with ngrok!
// ═══════════════════════════════════════════════════════════════

// ── STEP 1 ──────────────────────────────────────────────────────
// Add this at the very TOP of MapPage.jsx (after imports)
// Replace with your own ngrok URL after running: ngrok http 8001

const FASTAPI_URL = "https://YOUR-OWN-NGROK-URL.ngrok-free.app"

// ── STEP 2 ──────────────────────────────────────────────────────
// Add this state inside MapPage() after existing states:

const [floodHeatmap, setFloodHeatmap] = useState([])

// ── STEP 3 ──────────────────────────────────────────────────────
// Add this useEffect after your existing useEffects:

useEffect(() => {
  fetch(`${FASTAPI_URL}/ai/flood/heatmap`, {
    headers: { 'ngrok-skip-browser-warning': 'true' }
  })
    .then(res => res.json())
    .then(data => setFloodHeatmap(data.heatmap || []))
    .catch(err => console.warn("FastAPI offline:", err))
}, [])

// ── STEP 4 ──────────────────────────────────────────────────────
// Find this existing useEffect in MapPage.jsx:
//   useEffect(() => { rebuildLabels() }, [showRings])
// Change it to:
//   useEffect(() => { rebuildLabels() }, [showRings, floodHeatmap])

// ── STEP 5 ──────────────────────────────────────────────────────
// Inside rebuildLabels(), find the existing "if (showRings)" block.
// After the existing forEach, add this:

floodHeatmap.forEach(point => {
  const color =
    point.risk_level === 'High'   ? '#e84855' :
    point.risk_level === 'Medium' ? '#f4a35a' : '#00d68f'

  L.circle([point.lat, point.lng], {
    radius:      130,
    color:       color,
    fillColor:   color,
    fillOpacity: point.weight * 0.30,
    weight:      2.5,
    dashArray:   '6 4',
  }).addTo(lg).bindPopup(
    `<div style="min-width:160px">` +
    `<b style="font-size:14px">${point.zone}</b><br>` +
    `<span style="color:${color};font-weight:800">▲ ${point.risk_level} Flood Risk</span><br>` +
    `<hr style="margin:4px 0;opacity:.3">` +
    `🌊 Flood Incidents: <b>${point.flood_count}</b><br>` +
    `📊 AI Score: <b>${point.ai_score}</b>/100` +
    `</div>`
  )
})

// ── STEP 6 ──────────────────────────────────────────────────────
// Add this legend inside your map-fullwrap div in JSX return:

/*
<div style={{
  position:'absolute', bottom:70, right:12, zIndex:500,
  background:'rgba(19,29,48,.95)',
  border:'1px solid rgba(255,255,255,.12)',
  borderRadius:10, padding:'10px 14px',
  fontSize:12, color:'#fff'
}}>
  <div style={{fontWeight:800, marginBottom:6}}>🤖 AI Flood Risk</div>
  <div><span style={{color:'#e84855'}}>● </span>High Risk</div>
  <div><span style={{color:'#f4a35a'}}>● </span>Medium Risk</div>
  <div><span style={{color:'#00d68f'}}>● </span>Low Risk</div>
</div>
*/