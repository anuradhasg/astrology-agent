import React from 'react'

const CHIPS = [
  { emoji: '✨', text: "What's my zodiac sign if I was born June 12, 1994?" },
  { emoji: '🔮', text: "Today's horoscope for Leo" },
  { emoji: '💫', text: 'Are Scorpio and Cancer compatible?' },
  { emoji: '🌙', text: 'Tell me about Cancer traits and ruling planet' },
  { emoji: '♈', text: "What's the weekly horoscope for Aries?" },
  { emoji: '🌟', text: 'Is Aquarius a good match for Gemini?' },
]

export default function SuggestionChips({ onSelect }) {
  return (
    <div style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8,
      justifyContent: 'center',
      marginBottom: 24,
      animation: 'fadeUp 0.6s 0.25s ease both',
      animationFillMode: 'both',
    }}>
      {CHIPS.map(({ emoji, text }) => (
        <Chip key={text} emoji={emoji} text={text} onSelect={onSelect} />
      ))}
    </div>
  )
}

function Chip({ emoji, text, onSelect }) {
  const [hovered, setHovered] = React.useState(false)

  return (
    <button
      onClick={() => onSelect(text)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: hovered ? 'var(--mist)' : 'var(--cloud)',
        border: `1.5px solid ${hovered ? 'var(--breeze)' : 'var(--horizon)'}`,
        borderRadius: 20,
        padding: '7px 15px',
        fontSize: 13,
        color: hovered ? 'var(--deep)' : 'var(--dusk)',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        transform: hovered ? 'translateY(-2px)' : 'translateY(0)',
        boxShadow: hovered ? '0 4px 14px rgba(139,92,246,0.24)' : 'none',
        whiteSpace: 'nowrap',
        fontFamily: 'inherit',
      }}
    >
      {emoji} {text}
    </button>
  )
}
