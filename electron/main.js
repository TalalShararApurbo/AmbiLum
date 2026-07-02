import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants
const WLED_IP = '192.168.0.185';

const PRESETS_FILE = path.join(app.getPath('userData'), 'presets.json');
const SCENES_FILE = path.join(app.getPath('userData'), 'scenes.json');
const APP_STATE_FILE = path.join(app.getPath('userData'), 'app_state.json');

// --- WLED Logic ---
async function wledRequest(data) {
  try {
    const response = await fetch(`http://${WLED_IP}/json/state`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.ok;
  } catch (error) {
    console.error('WLED Request Error:', error);
    return false;
  }
}

// --- State Management ---
function readJSON(filePath, defaultData) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err);
  }
  return defaultData;
}

function writeJSON(filePath, data) {
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  } catch (err) {
    console.error(`Error writing ${filePath}:`, err);
  }
}

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1300,
    height: 850,
    title: 'AMBILUM - Dashboard',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // In development, load from Vite dev server. In production, load the built HTML.
  if (!app.isPackaged) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(async () => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// --- IPC Handlers ---

ipcMain.handle('wled:toggle', async (event, on) => {
  return await wledRequest({ on });
});

ipcMain.handle('wled:setBrightness', async (event, brightness) => {
  const bri = Math.max(0, Math.min(255, parseInt(brightness)));
  return await wledRequest({ bri });
});

ipcMain.handle('wled:setColor', async (event, hexColor) => {
  if (hexColor.startsWith('#')) hexColor = hexColor.slice(1);
  const r = parseInt(hexColor.slice(0, 2), 16);
  const g = parseInt(hexColor.slice(2, 4), 16);
  const b = parseInt(hexColor.slice(4, 6), 16);
  return await wledRequest({ seg: [{ col: [[r, g, b]] }] });
});

ipcMain.handle('wled:ping', async () => {
  try {
    const response = await fetch(`http://${WLED_IP}/json/state`, { timeout: 2000 });
    return response.status;
  } catch (error) {
    return 0;
  }
});

ipcMain.handle('data:read', (event, type) => {
  if (type === 'presets') return readJSON(PRESETS_FILE, { "Warm White": "#FFAA55", "Cool Blue": "#55AAFF" });
  if (type === 'scenes') return readJSON(SCENES_FILE, {
    "Study": { "color": "#3498DB" },
    "Gaming": { "color": "#E74C3C" },
    "Movie": { "color": "#9B59B6" },
    "Night": { "color": "#E67E22" }
  });
  if (type === 'appState') return readJSON(APP_STATE_FILE, { scenes: {}, devices: {}, wled_state: true });
});

ipcMain.handle('data:write', (event, type, data) => {
  if (type === 'presets') writeJSON(PRESETS_FILE, data);
  if (type === 'scenes') writeJSON(SCENES_FILE, data);
  if (type === 'appState') writeJSON(APP_STATE_FILE, data);
});
