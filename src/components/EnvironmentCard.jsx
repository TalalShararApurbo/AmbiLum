import React, { useState, useEffect } from 'react';
import { CloudRain } from 'lucide-react';

export default function EnvironmentCard({ lux }) {
  const [timeStr, setTimeStr] = useState('--:--');

  useEffect(() => {
    const timer = setInterval(() => {
      const d = new Date();
      setTimeStr(d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      
      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '30px 15px' }}>
        <div style={{ fontWeight: 'bold', color: 'var(--text-secondary)', marginBottom: '15px' }}>💡 Ambient Lux</div>
        <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{lux < 0 ? 'N/A' : (lux !== null && lux !== undefined) ? lux.toFixed(1) + ' lx' : 'Wait...'}</div>
      </div>

      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '30px 15px' }}>
        <div style={{ fontWeight: 'bold', color: 'var(--text-secondary)', marginBottom: '15px' }}>🕒 Local Time</div>
        <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{timeStr}</div>
      </div>
      
    </div>
  );
}
