module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        slate: { 950: '#0f172a', 900: '#0f172a' },
        indigo: { 400: '#818cf8', 500: '#6366f1', 600: '#4f46e5' },
        cyan: { 400: '#22d3ee', 500: '#06b6d4' },
        violet: { 500: '#a78bfa', 600: '#7c3aed' },
      },
      borderRadius: {
        '3xl': '1.5rem',
      },
      backdropBlur: {
        md: '12px',
      },
      boxShadow: {
        glow: '0 0 20px rgba(99, 102, 241, 0.4)',
        'glow-orange': '0 0 24px rgba(239, 68, 68, 0.5)',
        'glow-green': '0 0 24px rgba(16, 185, 129, 0.4)',
      },
      typography: {
        sm: {
          css: { fontSize: '0.875rem' },
        },
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
