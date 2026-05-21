import React from 'react';
import { Zap } from 'lucide-react';

export default function QuickActionsCard({ pingWled, pingSensor }) {
  return (
    <div className="glass-card">
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
        <button 
          className="btn" 
          onClick={pingWled}
          style={{ 
            height: '70px', 
            justifyContent: 'center', 
            alignItems: 'center', 
            flexDirection: 'column', 
            gap: '8px', 
            borderRadius: '16px',
            backgroundColor: '#3498DB',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.9rem',
            border: 'none'
          }}
        >
          <span style={{ fontSize: '1.4rem' }}>📡</span>
          Ping WLED
        </button>

        <button 
          className="btn" 
          onClick={pingSensor}
          style={{ 
            height: '70px', 
            justifyContent: 'center', 
            alignItems: 'center', 
            flexDirection: 'column', 
            gap: '8px', 
            borderRadius: '16px',
            backgroundColor: '#1ABC9C',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.9rem',
            border: 'none'
          }}
        >
          <span style={{ fontSize: '1.4rem' }}>📡</span>
          Ping Sensor
        </button>
      </div>
    </div>
  );
}
