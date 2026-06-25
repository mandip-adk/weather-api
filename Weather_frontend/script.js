// ── config ──
// change this if your Render URL is different
const API_BASE = 'https://weather-api-ugdj.onrender.com';

// ── element references ──
const els = {
  form: document.getElementById('searchForm'),
  input: document.getElementById('cityInput'),
  status: document.getElementById('statusMessage'),
  card: document.getElementById('weatherCard'),
  cityName: document.getElementById('cityName'),
  dateTime: document.getElementById('dateTime'),
  temperature: document.getElementById('temperature'),
  mercuryMarker: document.getElementById('mercuryMarker'),
  conditionIcon: document.getElementById('conditionIcon'),
  conditionText: document.getElementById('conditionText'),
  feelsLike: document.getElementById('feelsLike'),
  humidity: document.getElementById('humidity'),
  range: document.getElementById('range'),
  forecast: document.getElementById('forecastStrip'),
};

// ── icons (hand-drawn SVGs, no icon library needed) ─
const SUN = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.5 4.5l2 2M17.5 17.5l2 2M4.5 19.5l2-2M17.5 6.5l2-2"/></svg>`;
const CLOUD = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M7 18a4 4 0 0 1-.5-7.97A5 5 0 0 1 16 9a4.5 4.5 0 0 1 1 8.9"/><path d="M7 18h9"/></svg>`;
const RAIN = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M7 14a4 4 0 0 1-.5-7.97A5 5 0 0 1 16 5a4.5 4.5 0 0 1 1 8.9"/><path d="M8 18l-1 3M12 18l-1 3M16 18l-1 3"/></svg>`;
const STORM = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M7 13a4 4 0 0 1-.5-7.97A5 5 0 0 1 16 4a4.5 4.5 0 0 1 1 8.9"/><path d="M13 13l-3 5h3l-2 4"/></svg>`;
const SNOW = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M7 13a4 4 0 0 1-.5-7.97A5 5 0 0 1 16 4a4.5 4.5 0 0 1 1 8.9"/><path d="M8 18v3M8 18l-1.5 1M8 18l1.5 1M16 18v3M16 18l-1.5 1M16 18l1.5 1"/></svg>`;
const MIST = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 9h16M4 13h12M4 17h16"/></svg>`;

function iconFor(condition) {
  const c = (condition || '').toLowerCase();
  if (c.includes('clear')) return SUN;
  if (c.includes('thunder')) return STORM;
  if (c.includes('snow')) return SNOW;
  if (c.includes('rain') || c.includes('drizzle')) return RAIN;
  if (c.includes('mist') || c.includes('fog') || c.includes('haze')) return MIST;
  return CLOUD; // clouds, or anything unrecognized
}

// ── status / error display 
function showStatus(message, isError = false) {
  els.status.textContent = message;
  els.status.hidden = false;
  els.status.classList.toggle('error', isError);
  els.card.hidden = true;
  els.forecast.hidden = true;
}

function clearStatus() {
  els.status.hidden = true;
}

// ── the mercury marker position 
function setMercury(temp) {
  const min = -10, max = 45; // realistic range for clamping the marker
  const pct = Math.min(96, Math.max(4, ((temp - min) / (max - min)) * 100));
  els.mercuryMarker.style.bottom = pct + '%';
}

// ── render current weather into the card 
function renderWeather(data) {
  els.cityName.textContent = `${data.city}, ${data.country}`;
  els.dateTime.textContent = new Date().toLocaleString(undefined, {
    weekday: 'short', day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
  });
  els.temperature.textContent = `${Math.round(data.temperature)}°`;
  setMercury(data.temperature);
  els.conditionIcon.innerHTML = iconFor(data.condition);
  els.conditionText.textContent = data.condition;
  els.feelsLike.textContent = `${Math.round(data.feels_like)}°`;
  els.humidity.textContent = `${data.humidity}%`;
  els.range.textContent = `${Math.round(data.temp_min)}° – ${Math.round(data.temp_max)}°`;
  els.card.hidden = false;
}

// ── forecast comes back as 3-hour entries; pick one per day ──
function pickDailyEntries(list) {
  const byDate = {};
  list.forEach((entry) => {
    const [date, time] = entry.datetime.split(' ');
    const hour = parseInt(time.split(':')[0], 10);
    const existing = byDate[date];
    const existingHour = existing ? parseInt(existing.datetime.split(' ')[1].split(':')[0], 10) : null;

    // keep whichever entry for this date is closest to midday
    if (!existing || Math.abs(hour - 12) < Math.abs(existingHour - 12)) {
      byDate[date] = entry;
    }
  });
  return Object.values(byDate).slice(0, 5);
}

function renderForecast(forecastData) {
  const daily = pickDailyEntries(forecastData.forecast);
  els.forecast.innerHTML = '';

  daily.forEach((entry) => {
    const label = new Date(entry.datetime.replace(' ', 'T'))
      .toLocaleDateString(undefined, { weekday: 'short' });

    const day = document.createElement('div');
    day.className = 'forecast-day';
    day.innerHTML = `
      <div class="day-label">${label}</div>
      <div class="day-icon">${iconFor(entry.condition)}</div>
      <div class="day-high">${Math.round(entry.temperature)}°</div>
    `;
    els.forecast.appendChild(day);
  });

  els.forecast.hidden = false;
}

// ── main flow: fetch weather, then fetch forecast 
async function loadWeather(city) {
  showStatus('Reading station…');

  try {
    const weatherRes = await fetch(`${API_BASE}/api/weather/?city=${encodeURIComponent(city)}`);
    const weatherData = await weatherRes.json();

    if (!weatherRes.ok) {
      showStatus(weatherData.error || 'Station not found — check the spelling and try again.', true);
      return;
    }

    clearStatus();
    renderWeather(weatherData);

    const forecastRes = await fetch(`${API_BASE}/api/forecast/?city=${encodeURIComponent(city)}&days=5`);
    const forecastData = await forecastRes.json();

    if (forecastRes.ok) {
      renderForecast(forecastData);
    }
  } catch (err) {
    showStatus('Station offline — the API did not respond. Try again shortly.', true);
  }
}

// ── wire up the search form 
els.form.addEventListener('submit', (e) => {
  e.preventDefault();
  const city = els.input.value.trim();
  if (city) loadWeather(city);
});

// ── load a default city on page open 
loadWeather('Kathmandu');

