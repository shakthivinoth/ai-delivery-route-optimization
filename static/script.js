let avgSpeed = 30;
let map, layer;

// ---------- Navigation ----------
const titles = { dashboard: "Dashboard", route: "Route Optimizer", chat: "Safety Chatbot", policy: "Safety Policy", settings: "Settings" };
function showView(view) {
  document.querySelectorAll(".nav").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  document.querySelectorAll("[data-views]").forEach(c => c.classList.toggle("hidden", !c.dataset.views.split(" ").includes(view)));
  document.getElementById("grid").classList.toggle("two", view === "dashboard");
  document.getElementById("page-title").textContent = titles[view];
  setTimeout(() => map && map.invalidateSize(), 100);   // fix map size after showing
}
document.querySelectorAll(".nav").forEach(b => b.addEventListener("click", () => showView(b.dataset.view)));

// ---------- Map + Route ----------
function initMap() {
  map = L.map("map").setView([13.09, 80.26], 12);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "© OpenStreetMap contributors" }).addTo(map);
  layer = L.layerGroup().addTo(map);
}

async function optimizeRoute() {
  const customers = [...document.querySelectorAll(".customers input:checked")].map(c => c.value);
  const errBox = document.getElementById("error");
  errBox.textContent = "";
  try {
    const res = await fetch("/api/optimize", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ warehouse: document.getElementById("warehouse").value, customers, speed: avgSpeed })
    });
    const data = await res.json();
    if (!res.ok) { errBox.textContent = data.error; return; }
    document.getElementById("dist").textContent = data.total_distance_km + " km";
    document.getElementById("time").textContent = data.time_text;
    document.getElementById("speed").textContent = data.average_speed + " km/h";
    document.getElementById("route-text").textContent = data.route.join(" → ");
    drawRoute(data.coordinates, data.legs);
  } catch (e) { errBox.textContent = "Could not reach the server. Is app.py running?"; }
}

function drawRoute(points, legs) {
  layer.clearLayers();
  const latlngs = points.map(p => [p.lat, p.lng]);
  L.polyline(latlngs, { color: "#2563eb", weight: 5, opacity: 0.8 }).addTo(layer);
  points.forEach((p, i) => {
    const icon = L.divIcon({ className: "", html: `<div class="num-icon ${i === 0 ? "wh" : ""}">${i === 0 ? "W" : i}</div>`, iconSize: [28, 28] });
    const extra = i > 0 ? `<br>${legs[i - 1].km} km from previous stop` : "";
    L.marker([p.lat, p.lng], { icon }).bindPopup(`<b>${p.name}</b>${extra}`).addTo(layer);
  });
  map.fitBounds(latlngs, { padding: [40, 40] });
}

// ---------- Chatbot ----------
function addMessage(text, who, note) {
  const box = document.getElementById("messages");
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  if (note) { const s = document.createElement("small"); s.textContent = note; div.appendChild(s); }
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  try {
    const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: text }) });
    const data = await res.json();
    addMessage(data.answer, "bot", data.section ? "Policy section: " + data.section : null);
  } catch (e) { addMessage("Server not reachable.", "bot"); }
}

// ---------- Policy page ----------
async function loadPolicy() {
  const box = document.getElementById("policy-content");
  box.textContent = "";
  const data = await (await fetch("/api/policy")).json();
  for (const [heading, lines] of Object.entries(data)) {
    const sec = document.createElement("div");
    sec.className = "policy-section";
    const h = document.createElement("h3"); h.textContent = heading;
    const ul = document.createElement("ul");
    lines.forEach(l => { const li = document.createElement("li"); li.textContent = l; ul.appendChild(li); });
    sec.append(h, ul);
    box.appendChild(sec);
  }
}

// ---------- Settings ----------
document.getElementById("save-settings").addEventListener("click", () => {
  const v = parseFloat(document.getElementById("speed-input").value);
  const msg = document.getElementById("settings-msg");
  if (!(v > 0)) { msg.textContent = "Enter a speed greater than 0."; return; }
  avgSpeed = v;
  msg.textContent = `Saved. Average speed is now ${v} km/h. Click Optimize Route to recalculate.`;
});

// ---------- Start ----------
document.getElementById("optimize-btn").addEventListener("click", optimizeRoute);
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("chat-input").addEventListener("keydown", e => { if (e.key === "Enter") sendMessage(); });
initMap();
showView("dashboard");
optimizeRoute();
loadPolicy();
