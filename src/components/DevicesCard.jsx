import React, { useState } from 'react';
import { Power, X } from 'lucide-react';

function DeviceRow({ devId, name, state, toggleState, presets, scenes, assignDeviceScene, assignDevicePreset, currentColor, wheelListenerTarget, setWheelListenerTarget, applyWheelListener, cancelWheelListener, accentColor, showFullControls }) {
  const [showSlider, setShowSlider] = useState(false);
  const [presetVal, setPresetVal] = useState("");
  const [sceneVal, setSceneVal] = useState("");
  const [localBri, setLocalBri] = useState(255);

  const isListening = wheelListenerTarget && wheelListenerTarget.type === 'device' && wheelListenerTarget.id === devId;

  const commitBrightness = (val) => {
    if (devId === 'wled' && window.api) {
      window.api.wled.setBrightness(val);
    } else if (devId === 'twinkle' && window.api) {
      window.api.twinkle.setBrightness(val);
    }
  };

  return (
    <div className="list-item" style={{ border: '1px solid var(--glass-border)', backgroundColor: 'var(--bg-secondary)', display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontWeight: 'bold', fontSize: '1rem', color: 'var(--text-primary)' }}>{name}</span>
        <label className="switch" style={{ transform: 'scale(0.8)', transformOrigin: 'right' }}>
          <input type="checkbox" checked={state} onChange={toggleState} />
          <span className="slider" style={{ backgroundColor: accentColor }}></span>
        </label>
      </div>

      <div style={{ display: 'flex', gap: '6px', marginTop: '10px', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
        
        {showSlider ? (
          <div style={{ display: 'flex', width: '100%', alignItems: 'center', gap: '10px', padding: '0px', minHeight: '34px' }}>
            <span style={{ fontWeight: 'bold', fontSize: '0.85rem' }}>{Math.round((localBri / 255) * 100)}%</span>
            <input type="range" min="0" max="255" value={localBri} onChange={(e) => {
              const v = parseInt(e.target.value);
              setLocalBri(v);
              commitBrightness(v);
            }} style={{ flex: 1 }} />
            <button className="btn btn-primary" onClick={() => {
              setLocalBri(127);
              commitBrightness(127);
            }}>Auto</button>
            <button className="btn btn-danger" onClick={() => setShowSlider(false)}><X size={14} /></button>
          </div>
        ) : (
          <>
            {showFullControls && (
              <>
                <select className="input-text" value={sceneVal} style={{ maxWidth: '85px' }} onChange={(e) => {
                  if(e.target.value) {
                    assignDeviceScene(devId, e.target.value);
                    setSceneVal(e.target.value);
                    setPresetVal("");
                    if(isListening) cancelWheelListener();
                  }
                }}>
                  <option value="">{sceneVal || "Scenes..."}</option>
                  {Object.keys(scenes).map(s => <option key={s} value={s}>{s}</option>)}
                </select>

                <select className="input-text" value={presetVal} style={{ maxWidth: '85px' }} onChange={(e) => {
                  if(e.target.value) {
                    assignDevicePreset(devId, e.target.value);
                    setPresetVal(e.target.value);
                    setSceneVal("");
                    if(isListening) cancelWheelListener();
                  }
                }}>
                  <option value="">{presetVal || "Presets..."}</option>
                  {Object.keys(presets).map(p => <option key={p} value={p}>{p}</option>)}
                </select>

                {!isListening ? (
                  <button className="btn" onClick={() => setWheelListenerTarget({ type: 'device', id: devId })}>🎨 Wheel</button>
                ) : (
                  <>
                    <button className="btn" onClick={() => { applyWheelListener(); setSceneVal(""); setPresetVal(""); assignDeviceScene(devId, null); }} style={{ backgroundColor: currentColor, color: '#fff', border: 'none', fontWeight: 'bold' }}>SET</button>
                    <button className="btn btn-danger" onClick={() => cancelWheelListener()}><X size={14} /></button>
                  </>
                )}
              </>
            )}
            
            <button className="btn" onClick={() => setShowSlider(true)}>
              {Math.round((localBri / 255) * 100)}% 🔅
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default function DevicesCard({ wledOn, handleToggleWLED, presets, scenes, assignDeviceScene, assignDevicePreset, currentColor, wheelListenerTarget, setWheelListenerTarget, applyWheelListener, cancelWheelListener }) {
  return (
    <div className="glass-card" style={{ flex: 1, minHeight: 0 }}>
      <div className="card-header">
        <Power size={24} />
        <h2 className="card-title">Devices</h2>
      </div>
      
      <div className="card-scroll-area">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          
          <DeviceRow 
            devId="twinkle" name="✨ Twinkle Tray" state={false} toggleState={() => {}} 
            presets={presets} scenes={scenes} accentColor="#9370DB" showFullControls={false}
          />
          <DeviceRow 
            devId="openrgb" name="💻 OpenRGB" state={true} toggleState={() => {}} 
            presets={presets} scenes={scenes} accentColor="#1E90FF" showFullControls={true}
            assignDeviceScene={assignDeviceScene} assignDevicePreset={assignDevicePreset}
            currentColor={currentColor} wheelListenerTarget={wheelListenerTarget} setWheelListenerTarget={setWheelListenerTarget} applyWheelListener={applyWheelListener} cancelWheelListener={cancelWheelListener}
          />
          <DeviceRow 
            devId="wled" name="🌐 WLED" state={wledOn} toggleState={handleToggleWLED} 
            presets={presets} scenes={scenes} accentColor="#FFA500" showFullControls={true}
            assignDeviceScene={assignDeviceScene} assignDevicePreset={assignDevicePreset}
            currentColor={currentColor} wheelListenerTarget={wheelListenerTarget} setWheelListenerTarget={setWheelListenerTarget} applyWheelListener={applyWheelListener} cancelWheelListener={cancelWheelListener}
          />

        </div>
      </div>
      
      <button className="btn" style={{ width: '100%', marginTop: '20px', justifyContent: 'center', border: '1px solid var(--text-secondary)' }}>
        ➕ Add Device
      </button>
    </div>
  );
}
