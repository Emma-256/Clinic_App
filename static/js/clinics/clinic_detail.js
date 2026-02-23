const mapElement = document.getElementById('map');
const lat = parseFloat(mapElement.dataset.lat);
const lng = parseFloat(mapElement.dataset.lng);
const name = mapElement.dataset.name;
const location = mapElement.dataset.location;

var map = L.map('map').setView([lat, lng], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var icon = L.divIcon({
  html: `<div style="
    background:#0a7c6e; width:36px; height:36px; border-radius:50% 50% 50% 0;
    transform:rotate(-45deg); border:3px solid #fff;
    box-shadow:0 2px 10px rgba(0,0,0,.3);
  "></div>`,
  className: '',
  iconSize: [36, 36],
  iconAnchor: [18, 36],
  popupAnchor: [0, -38]
});

L.marker([lat, lng], {icon})
  .addTo(map)
  .bindPopup(`
    <div style="font-family:'Sora',sans-serif;padding:4px 2px;min-width:140px;">
      <strong style="font-size:.9rem;color:#0f4c40;">${name}</strong><br>
      <span style="font-size:.78rem;color:#64748b;">${location}</span>
    </div>
  `)
  .openPopup();
