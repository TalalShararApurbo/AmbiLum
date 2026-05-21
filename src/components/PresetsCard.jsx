import React, { useState } from 'react';
import { Settings, Trash2, Check, X } from 'lucide-react';

function PresetRow({ name, pColor, deletePreset }) {
  const [confirmDelete, setConfirmDelete] = useState(false);

  return (
    <div className="list-item" style={{ backgroundColor: pColor, border: '1px solid rgba(255,255,255,0.2)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontWeight: 600, color: '#fff', textShadow: '0px 0px 4px rgba(0,0,0,0.8)' }}>{name}</span>
      </div>
      <div style={{ display: 'flex', gap: '6px' }}>
        {!confirmDelete ? (
          <button className="btn btn-danger preset-btn" onClick={() => setConfirmDelete(true)}><Trash2 size={14} /></button>
        ) : (
          <>
            <button className="btn btn-success preset-btn" onClick={() => { deletePreset(name); setConfirmDelete(false); }}><Check size={14} /></button>
            <button className="btn btn-danger preset-btn" onClick={() => setConfirmDelete(false)}><X size={14} /></button>
          </>
        )}
      </div>
    </div>
  );
}

export default function PresetsCard({ presets, deletePreset }) {
  return (
    <div className="glass-card" style={{ flex: 1, minHeight: 0 }}>
      <div className="card-header">
        <Settings size={24} />
        <h2 className="card-title">Presets</h2>
      </div>
      
      <div className="card-scroll-area">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {Object.entries(presets).map(([name, pColor]) => (
            <PresetRow key={name} name={name} pColor={pColor} deletePreset={deletePreset} />
          ))}
          {Object.keys(presets).length === 0 && (
            <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>No presets saved.</p>
          )}
        </div>
      </div>
    </div>
  );
}
