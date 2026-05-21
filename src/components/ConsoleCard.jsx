import React, { useEffect, useRef } from 'react';
import { RefreshCw } from 'lucide-react';

export default function ConsoleCard({ logs }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="glass-card" style={{ flex: 1, minHeight: 0 }}>
      <div className="card-header">
        <RefreshCw size={24} />
        <h2 className="card-title">🖥️ Console</h2>
      </div>
      
      <div style={{ 
          backgroundColor: 'var(--bg-secondary)', 
          border: '1px solid var(--glass-border)',
          borderRadius: '12px',
          padding: '10px 5px 10px 10px',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: 0
      }}>
        <div ref={scrollRef} className="card-scroll-area" style={{ 
            fontFamily: 'Consolas, monospace',
            fontSize: '11px',
            color: '#4ade80'
        }}>
          <p>System Initialized.</p>
          <p>Waiting for commands...</p>
          {logs.map((log, i) => {
            let logColor = '#4ade80'; // default Matrix green
            if (log.includes('❌') || log.includes('Failed') || log.includes('Error') || log.includes('OFFLINE')) {
              logColor = '#ff4444'; // Red
            } else if (log.includes('⚠️') || log.includes('TIMEOUT')) {
              logColor = '#FFA500'; // Orange
            } else if (log.includes('✅') || log.includes('ONLINE') || log.includes('OK')) {
              logColor = '#10B981'; // Bright Green
            }
            return <p key={i} style={{ margin: '2px 0', color: logColor }}>{log}</p>;
          })}
        </div>
      </div>
    </div>
  );
}
