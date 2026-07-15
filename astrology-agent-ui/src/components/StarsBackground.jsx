import React, { useMemo } from 'react'

function randomStars(count) {
  const stars = []
  for (let i = 0; i < count; i++) {
    stars.push({
      top: Math.random() * 100,
      left: Math.random() * 100,
      size: Math.random() * 2 + 1,
      dur: (Math.random() * 2.5 + 2).toFixed(2),
      delay: (Math.random() * 3).toFixed(2),
    })
  }
  return stars
}

export default function StarsBackground() {
  const stars = useMemo(() => randomStars(140), [])

  return (
    <div style={{
      position: 'fixed', inset: 0, pointerEvents: 'none',
      zIndex: 0, overflow: 'hidden',
    }}>
      {/* Nebula gradient */}
      <div style={{
        position: 'absolute', inset: 0,
        background: `
          radial-gradient(ellipse 80% 40% at 20% -10%, rgba(139,92,246,0.16) 0%, transparent 70%),
          radial-gradient(ellipse 60% 30% at 85% 5%, rgba(212,175,55,0.10) 0%, transparent 60%),
          linear-gradient(180deg, #0B0B1F 0%, #12102A 100%)
        `,
      }} />

      {/* Stars */}
      {stars.map((s, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            top: `${s.top}%`,
            left: `${s.left}%`,
            width: s.size,
            height: s.size,
            borderRadius: '50%',
            background: '#FFFFFF',
            animation: `twinkle ${s.dur}s ease-in-out infinite`,
            animationDelay: `${s.delay}s`,
          }}
        />
      ))}
    </div>
  )
}
