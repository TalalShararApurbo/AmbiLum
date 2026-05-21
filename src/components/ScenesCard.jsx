import React, { useState } from 'react';
import { Moon, Trash2, Check, X, Save } from 'lucide-react';

function SceneRow({ name, data, deleteScene, presets, saveScene, currentColor, wheelListenerTarget, setWheelListenerTarget, applyWheelListener, cancelWheelListener }) {
  const [confirmDelete, setConfirmDelete] = useState(false);
  
  const presetName = data.presetName || "";
  const isListening = wheelListenerTarget && wheelListenerTarget.type === 'scene' && wheelListenerTarget.id === name;

  return (
    <div className="list-item">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ width: 20, height: 20, borderRadius: '50%', backgroundColor: data.color || '#fff' }}></div>
        <span style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{name}</span>
      </div>
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        
        {!confirmDelete ? (
          <button className="btn btn-danger" style={{ padding: '6px 8px' }} onClick={() => setConfirmDelete(true)}><Trash2 size={14} /></button>
        ) : (
          <div style={{ display: 'flex', gap: '5px' }}>
            <button className="btn btn-success" style={{ padding: '6px 8px' }} onClick={() => { deleteScene(name); setConfirmDelete(false); }}><Check size={14} /></button>
            <button className="btn btn-danger" style={{ padding: '6px 8px' }} onClick={() => setConfirmDelete(false)}><X size={14} /></button>
          </div>
        )}

        <div style={{ display: 'flex', gap: '5px' }}>
          {!isListening ? (
            <button className="btn" onClick={() => setWheelListenerTarget({ type: 'scene', id: name })}>🎨 Wheel</button>
          ) : (
            <>
              <button className="btn" onClick={() => { applyWheelListener(); }} style={{ backgroundColor: currentColor, color: '#fff', border: '1px solid transparent', fontWeight: 'bold' }}>SET</button>
              <button className="btn btn-danger" onClick={() => cancelWheelListener()}><X size={14} /></button>
            </>
          )}
        </div>

        <select className="input-text" value={presetName} style={{ maxWidth: '90px' }} onChange={(e) => {
          if (e.target.value) {
            saveScene(name, presets[e.target.value], e.target.value);
            if(isListening) cancelWheelListener();
          }
        }}>
          <option value="">{presetName || "Presets..."}</option>
          {Object.keys(presets).map(p => <option key={p} value={p}>{p}</option>)}
        </select>
        
      </div>
    </div>
  );
}

export default function ScenesCard({ scenes, deleteScene, presets, saveScene, currentColor, wheelListenerTarget, setWheelListenerTarget, applyWheelListener, cancelWheelListener }) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [sceneName, setSceneName] = useState('');
  const [sceneColor, setSceneColor] = useState(currentColor);
  const [scenePreset, setScenePreset] = useState('');

  return (
    <div className="glass-card" style={{ flex: 1, minHeight: 0 }}>
      <div className="card-header">
        <Moon size={24} />
        <h2 className="card-title">Scenes</h2>
      </div>
      
      <div className="card-scroll-area">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {Object.entries(scenes).map(([name, data]) => (
            <SceneRow key={name} name={name} data={data} deleteScene={deleteScene} presets={presets} saveScene={saveScene} currentColor={currentColor} wheelListenerTarget={wheelListenerTarget} setWheelListenerTarget={setWheelListenerTarget} applyWheelListener={applyWheelListener} cancelWheelListener={cancelWheelListener} />
          ))}
        </div>
      </div>
      
      {!showAddForm ? (
        <button className="btn" style={{ width: '100%', marginTop: '20px', justifyContent: 'center', border: '1px solid var(--text-secondary)' }} onClick={() => setShowAddForm(true)}>
          ➕ Add Scene
        </button>
      ) : (
        <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <button className="btn btn-danger" style={{ justifyContent: 'center' }} onClick={() => setShowAddForm(false)}>❌ Cancel</button>
          <input className="input-text" placeholder="Scene Name..." value={sceneName} onChange={e => setSceneName(e.target.value)} />
          <div style={{ display: 'flex', gap: '10px' }}>
            
            {!(wheelListenerTarget && wheelListenerTarget.type === 'new_scene') ? (
              <button className="btn" style={{ flex: 1 }} onClick={() => setWheelListenerTarget({ type: 'new_scene' })}>🎨 Pick Wheel Color</button>
            ) : (
              <div style={{ display: 'flex', flex: 1, gap: '5px' }}>
                <button className="btn" style={{ flex: 1, backgroundColor: currentColor, color: '#fff', border: '1px solid transparent', fontWeight: 'bold' }} onClick={() => { setSceneColor(currentColor); setScenePreset(''); cancelWheelListener(); }}>SET</button>
                <button className="btn btn-danger" onClick={() => cancelWheelListener()}><X size={14} /></button>
              </div>
            )}

            <select className="input-text" value={scenePreset} style={{ flex: 1 }} onChange={(e) => {
              setSceneColor(presets[e.target.value]);
              setScenePreset(e.target.value);
            }}>
              <option value="">Presets...</option>
              {Object.keys(presets).map(p => <option key={p} value={p}>{p}</option>)}
            </select>
            <button className="btn btn-primary" onClick={() => { saveScene(sceneName, sceneColor, scenePreset); setSceneName(''); setScenePreset(''); setShowAddForm(false); }}>
              <Save size={14} /> Save
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
