import React from 'react';

export default function SettingsCard() {
  const sampleData = [
    { timestamp: "2026-05-18 10:00:00 AM", lux: "320 lx", profile: "Study", source: "Rule Engine" },
    { timestamp: "2026-05-18 11:30:15 AM", lux: "450 lx", profile: "Daylight Auto", source: "Rule Engine" },
    { timestamp: "2026-05-18 02:10:00 PM", lux: "280 lx", profile: "Gaming", source: "User Override" },
    { timestamp: "2026-05-18 06:00:00 PM", lux: "150 lx", profile: "Warm Evening", source: "Rule Engine" },
    { timestamp: "2026-05-18 09:00:00 PM", lux: "50 lx",  profile: "Night", source: "Rule Engine" },
  ];

  return (
    <div className="glass-card" style={{ flex: 1 }}>
      <h2 className="card-title" style={{ fontSize: '1.5rem', marginBottom: '20px' }}>System Data & Settings</h2>
      
      <div style={{ backgroundColor: 'var(--bg-secondary)', borderRadius: '25px', border: '1px solid var(--glass-border)', padding: '15px', flex: 1, display: 'flex', flexDirection: 'column' }}>
        
        {/* Header */}
        <div style={{ display: 'flex', padding: '10px 15px', color: 'var(--text-secondary)', fontWeight: 'bold', fontSize: '12px' }}>
          <div style={{ flex: 2 }}>TIMESTAMP</div>
          <div style={{ flex: 1 }}>LUX</div>
          <div style={{ flex: 2 }}>PROFILE</div>
          <div style={{ flex: 2 }}>DECISION SOURCE</div>
        </div>

        {/* Scrollable Rows */}
        <div className="card-scroll-area">
          {sampleData.map((row, idx) => (
            <div key={idx} style={{ 
              display: 'flex', 
              padding: '12px 15px', 
              backgroundColor: idx % 2 === 0 ? 'rgba(0,0,0,0.02)' : 'rgba(0,0,0,0.05)',
              borderRadius: '8px',
              marginBottom: '4px',
              alignItems: 'center'
            }}>
              <div style={{ flex: 2, fontWeight: 500 }}>{row.timestamp}</div>
              <div style={{ flex: 1 }}>{row.lux}</div>
              <div style={{ flex: 2 }}>{row.profile}</div>
              <div style={{ flex: 2, color: row.source.includes('Override') ? 'var(--danger)' : 'var(--success)' }}>
                {row.source}
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
