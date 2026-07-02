import React from 'react';
import { Zap } from 'lucide-react';

export default function QuickActionsCard({ pingTwinkle, pingWled, pingSensor }) {
  return (
    <div className="glass-card">
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
        <button 
          className="btn" 
          onClick={pingTwinkle}
          style={{ 
            height: '65px', 
            justifyContent: 'center', 
            alignItems: 'center', 
            flexDirection: 'column', 
            gap: '4px', 
            borderRadius: '14px',
            backgroundColor: '#9B59B6',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.8rem',
            border: 'none'
          }}
        >
          <span style={{ fontSize: '1.2rem' }}>✨</span>
          Twinkle
        </button>

        <button 
          className="btn" 
          onClick={pingWled}
          style={{ 
            height: '65px', 
            justifyContent: 'center', 
            alignItems: 'center', 
            flexDirection: 'column', 
            gap: '4px', 
            borderRadius: '14px',
            backgroundColor: '#3498DB',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.8rem',
            border: 'none'
          }}
        >
          <span style={{ fontSize: '1.2rem' }}>📡</span>
          WLED
        </button>

        <button 
          className="btn" 
          onClick={pingSensor}
          style={{ 
            height: '65px', 
            justifyContent: 'center', 
            alignItems: 'center', 
            flexDirection: 'column', 
            gap: '4px', 
            borderRadius: '14px',
            backgroundColor: '#1ABC9C',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '0.8rem',
            border: 'none'
          }}
        >
          <span style={{ fontSize: '1.2rem' }}>📡</span>
          Sensor
        </button>
      </div>
    </div>
  );
}
