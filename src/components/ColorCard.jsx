import React, { useState } from 'react';
import Wheel from '@uiw/react-color-wheel';
import { Palette, Save } from 'lucide-react';

export default function ColorCard({ color, setColor, handleColorChange, wledBri, handleBrightnessChange, savePreset }) {
  const [presetName, setPresetName] = useState('');

  return (
    <div className="glass-card">
      <div className="card-header">
        <Palette size={24} />
        <h2 className="card-title">Color Wheel</h2>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '15px', padding: '5px 0' }}>
        <Wheel
          color={color}
          onChange={(colorObj) => {
            setColor(colorObj.hex);
            handleColorChange(colorObj.hex);
          }}
          width={150}
          height={150}
        />
        
        <input 
          type="text" 
          value={color}
          onChange={(e) => {
            setColor(e.target.value);
            if(e.target.value.length === 7 && e.target.value.startsWith('#')){
              handleColorChange(e.target.value);
            }
          }}
          style={{
            width: '100%', maxWidth: '150px', height: '32px', textAlign: 'center',
            fontSize: '1rem', fontWeight: 'bold', borderRadius: '16px',
            backgroundColor: color, color: '#fff', border: 'none',
            textShadow: '0px 0px 4px rgba(0,0,0,0.8)'
          }}
        />
      </div>

      <div style={{ marginTop: '10px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <span style={{ fontWeight: 600 }}>Brightness</span>
          <span style={{ fontWeight: 'bold' }}>{Math.round((wledBri / 255) * 100)}%</span>
        </div>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
          <input 
            type="range" 
            min="0" max="255" 
            value={wledBri} 
            onChange={handleBrightnessChange} 
            style={{ flex: 1 }}
          />
          <button className="btn btn-primary" onClick={() => handleBrightnessChange({target: {value: 127}})}>Auto</button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '30px' }}>
        <input 
          type="text" 
          className="input-text" 
          placeholder="Preset Name..." 
          value={presetName}
          onChange={(e) => setPresetName(e.target.value)}
          style={{ flex: 1 }}
        />
        <button className="btn btn-primary" onClick={() => {
          savePreset(presetName);
          setPresetName('');
        }}>
          <Save size={18} /> Save
        </button>
      </div>
    </div>
  );
}
