import React, { useState, useEffect } from 'react';
import { Settings, Sun, Moon, Home } from 'lucide-react';
import './index.css';

import ColorCard from './components/ColorCard';
import PresetsCard from './components/PresetsCard';
import ScenesCard from './components/ScenesCard';
import DevicesCard from './components/DevicesCard';
import ConsoleCard from './components/ConsoleCard';
import EnvironmentCard from './components/EnvironmentCard';
import CalibrationCard from './components/CalibrationCard';
import QuickActionsCard from './components/QuickActionsCard';
import SettingsCard from './components/SettingsCard';

function App() {
  const [view, setView] = useState('home');
  const [lux, setLux] = useState(0);
  const [lastSensorUpdate, setLastSensorUpdate] = useState(0);
  
  const [wledOn, setWledOn] = useState(true);
  
  const [colorCardBri, setColorCardBri] = useState(255);
  
  const [color, setColor] = useState('#FFA500');
  
  const [presets, setPresets] = useState({});
  const [scenes, setScenes] = useState({});
  const [logs, setLogs] = useState([]);
  const [theme, setTheme] = useState('dark');

  const [deviceScenes, setDeviceScenes] = useState({ wled: null, openrgb: null, twinkle: null });

  const [wheelListenerTarget, setWheelListenerTarget] = useState(null);
  
  const [isLoaded, setIsLoaded] = useState(false);

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${time}] ${msg}`].slice(-50));
  };

  useEffect(() => {
    if (theme === 'light') {
      document.body.classList.add('light-mode');
    } else {
      document.body.classList.remove('light-mode');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  useEffect(() => {
    if (window.api) {
      Promise.all([
        window.api.data.read('presets'),
        window.api.data.read('scenes'),
        window.api.data.read('appState')
      ]).then(([presetsData, scenesData, appStateData]) => {
        if (presetsData) setPresets(presetsData);
        if (scenesData) setScenes(scenesData);
        if (appStateData) {
          if (appStateData.theme) setTheme(appStateData.theme);
          if (appStateData.wledOn !== undefined) setWledOn(appStateData.wledOn);
          if (appStateData.color) setColor(appStateData.color);
          if (appStateData.colorCardBri !== undefined) setColorCardBri(appStateData.colorCardBri);
          if (appStateData.deviceScenes) setDeviceScenes(appStateData.deviceScenes);
        }
        setIsLoaded(true);
      });

      if (window.api.onLuxUpdate) {
        const unsubscribe = window.api.onLuxUpdate((luxVal) => {
          setLux(luxVal);
          setLastSensorUpdate(Date.now());
        });
        return unsubscribe;
      }
    } else {
      setIsLoaded(true);
    }
  }, []);

  useEffect(() => {
    if (isLoaded && window.api) {
      window.api.data.write('appState', { theme, wledOn, color, colorCardBri, deviceScenes });
    }
  }, [isLoaded, theme, wledOn, color, colorCardBri, deviceScenes]);

  useEffect(() => {
    if (isLoaded && window.api) window.api.data.write('presets', presets);
  }, [isLoaded, presets]);

  useEffect(() => {
    if (isLoaded && window.api) window.api.data.write('scenes', scenes);
  }, [isLoaded, scenes]);

  const handleToggleWLED = async () => {
    const newState = !wledOn;
    setWledOn(newState);
    addLog(`WLED Power: ${newState ? 'ON' : 'OFF'}`);
    if (window.api) {
      await window.api.wled.toggle(newState);
    }
  };

  const [wledColorState, setWledColorState] = useState('#FFA500');
  const [originalWledColor, setOriginalWledColor] = useState('#FFA500');

  const commitWledColor = (newColor) => {
    setWledColorState(newColor);
    setOriginalWledColor(newColor);
    if (window.api && wledOn) window.api.wled.setColor(newColor);
  };

  const startWheelListener = (target) => {
    if (target.type === 'device' && target.id === 'wled') {
      setOriginalWledColor(wledColorState);
      if (window.api && wledOn) window.api.wled.setColor(color);
    }
    setWheelListenerTarget(target);
  };

  const handleColorChange = (newColor) => {
    setColor(newColor);
    if (wheelListenerTarget && wheelListenerTarget.type === 'device' && wheelListenerTarget.id === 'wled') {
      if (window.api && wledOn) window.api.wled.setColor(newColor);
    }
  };

  const applyWheelListener = () => {
    if (!wheelListenerTarget) return;
    const { type, id } = wheelListenerTarget;
    
    if (type === 'device') {
      addLog(`Setting ${id} to wheel color (${color})`);
      if (id === 'wled') commitWledColor(color);
    } else if (type === 'scene') {
      saveScene(id, color, null);
    }
    
    setWheelListenerTarget(null);
  };

  const cancelWheelListener = () => {
    if (wheelListenerTarget && wheelListenerTarget.type === 'device' && wheelListenerTarget.id === 'wled') {
      if (window.api && wledOn) window.api.wled.setColor(originalWledColor);
    }
    setWheelListenerTarget(null);
  };

  const handleColorCardBrightness = (e) => {
    setColorCardBri(parseInt(e.target.value));
  };

  const savePreset = (name) => {
    if (!name.trim()) return;
    const updated = { ...presets, [name]: color };
    setPresets(updated);
    addLog(`Saved preset: ${name}`);
  };

  const applyPreset = (name) => {
    const pColor = presets[name];
    if (pColor) {
      setColor(pColor);
      addLog(`Loaded preset ${name} to Color Wheel`);
    }
  };

  const deletePreset = (name) => {
    const updated = { ...presets };
    delete updated[name];
    setPresets(updated);
    addLog(`Deleted preset: ${name}`);
  };

  const saveScene = (name, sceneColor, presetName = null) => {
    if (!name.trim()) return;
    const updated = { ...scenes, [name]: { color: sceneColor, presetName } };
    setScenes(updated);
    addLog(`Saved scene: ${name}`);

    if (deviceScenes.wled === name) {
      commitWledColor(sceneColor);
      addLog(`WLED color sync'd to updated scene ${name}`);
    }
  };

  const deleteScene = (name) => {
    const updated = { ...scenes };
    delete updated[name];
    setScenes(updated);
    addLog(`Deleted scene: ${name}`);
  };

  const assignDeviceScene = (devId, sceneName) => {
    setDeviceScenes(prev => ({ ...prev, [devId]: sceneName }));
    if (sceneName && scenes[sceneName]) {
      addLog(`${devId} assigned to scene: ${sceneName}`);
      if (devId === 'wled') {
        commitWledColor(scenes[sceneName].color);
      }
    }
  };

  const assignDevicePreset = (devId, presetName) => {
    setDeviceScenes(prev => ({ ...prev, [devId]: null }));
    if (presetName && presets[presetName]) {
      addLog(`${devId} assigned to preset: ${presetName}`);
      if (devId === 'wled') {
        commitWledColor(presets[presetName]);
      }
    }
  };

  const pingWled = async () => {
    addLog(`Pinging WLED...`);
    if (window.api) {
      const status = await window.api.wled.ping();
      if (status === 200) {
        addLog(`✅ WLED Responded: OK (200)`);
      } else {
        addLog(`❌ WLED Ping Failed (${status})`);
      }
    }
  };

  const pingSensor = () => {
    addLog(`Pinging ESP8266 Sensor via MQTT...`);
    const timeSinceLastUpdate = Date.now() - lastSensorUpdate;
    if (lastSensorUpdate === 0) {
      addLog(`❌ SENSOR OFFLINE: No signal received from ESP8266. Board may be unpowered.`);
    } else if (timeSinceLastUpdate > 5000) {
      addLog(`⚠️ SENSOR TIMEOUT: Last signal was ${Math.floor(timeSinceLastUpdate / 1000)}s ago. ESP8266 connection lost.`);
    } else if (lux < 0) {
      addLog(`⚠️ BOARD ONLINE: ESP8266 connected, but BH1750 Sensor is missing!`);
    } else {
      addLog(`✅ SENSOR ONLINE: Connection stable. Packet received ${timeSinceLastUpdate}ms ago.`);
    }
  };

  // Derived active scene for WLED to show in Header
  const activeWledScene = deviceScenes.wled || 'N/A';

  return (
    <div className="app-container">
      <header className="header glass-card" style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-start', alignItems: 'center', gap: '15px' }}>
          <span style={{ color: 'var(--success)', fontWeight: 'bold', fontSize: '0.9rem' }}>
            Detected Scene: {activeWledScene}
          </span>
          <span className={`status-badge ${wledOn ? '' : 'offline'}`}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: 'currentColor', display: 'inline-block' }}></span>
            WLED {wledOn ? 'Connected' : 'Offline'}
          </span>
        </div>
        
        <h1 style={{ margin: 0, flex: 1, textAlign: 'center', fontFamily: "'Orbitron', sans-serif", letterSpacing: '4px' }}>AMBILUM</h1>
        
        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '8px' }}>
          <button className="btn" onClick={toggleTheme} style={{ borderRadius: '50%', padding: '8px' }}>
            {theme === 'dark' ? <Sun size={16} /> : <Moon size={16} />}
          </button>
          <button className="btn" onClick={() => setView(view === 'home' ? 'settings' : 'home')} style={{ borderRadius: '50%', padding: '8px' }}>
            {view === 'home' ? <Settings size={16} /> : <Home size={16} />}
          </button>
        </div>
      </header>

      {view === 'home' ? (
        <div className="dashboard-grid">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflow: 'hidden' }}>
            <ColorCard 
              color={color} 
              setColor={setColor} 
              handleColorChange={handleColorChange} 
              wledBri={colorCardBri} 
              handleBrightnessChange={handleColorCardBrightness} 
              savePreset={savePreset}
            />
            <PresetsCard 
              presets={presets} 
              deletePreset={deletePreset}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflow: 'hidden' }}>
            <EnvironmentCard lux={lux} />
            <ScenesCard 
              scenes={scenes} 
              deleteScene={deleteScene}
              presets={presets}
              saveScene={saveScene}
              currentColor={color}
              wheelListenerTarget={wheelListenerTarget}
              setWheelListenerTarget={startWheelListener}
              applyWheelListener={applyWheelListener}
              cancelWheelListener={cancelWheelListener}
            />
            <CalibrationCard />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflow: 'hidden' }}>
            <DevicesCard 
              wledOn={wledOn} 
              handleToggleWLED={handleToggleWLED}
              presets={presets}
              scenes={scenes}
              assignDeviceScene={assignDeviceScene}
              assignDevicePreset={assignDevicePreset}
              currentColor={color}
              wheelListenerTarget={wheelListenerTarget}
              setWheelListenerTarget={startWheelListener}
              applyWheelListener={applyWheelListener}
              cancelWheelListener={cancelWheelListener}
            />
            <QuickActionsCard 
              pingWled={pingWled} 
              pingSensor={pingSensor} 
            />
            <ConsoleCard logs={logs} />
          </div>
        </div>
      ) : (
        <SettingsCard />
      )}
    </div>
  );
}

export default App;
