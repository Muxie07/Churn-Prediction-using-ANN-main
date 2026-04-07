import React from 'react';

const GaugeChart = ({ value = 42 }) => {
  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (value / 100) * circumference;
  const rotation = value * 1.8 - 90;

  return (
    <svg width="200" height="200" viewBox="0 0 200 200" className="drop-shadow-lg">
      {/* Background Circle */}
      <circle cx="100" cy="100" r="45" fill="none" stroke="rgba(148,163,184,0.1)" strokeWidth="8" />
      
      {/* Progress Circle with Glow */}
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#10b981" />
          <stop offset="50%" stopColor="#f59e0b" />
          <stop offset="100%" stopColor="#ef4444" />
        </linearGradient>
      </defs>
      
      <circle
        cx="100"
        cy="100"
        r="45"
        fill="none"
        stroke="url(#gaugeGradient)"
        strokeWidth="8"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        filter="url(#glow)"
        style={{ transition: 'stroke-dashoffset 0.6s ease' }}
      />

      {/* Center Value */}
      <text x="100" y="95" textAnchor="middle" fontSize="28" fontWeight="bold" fill="#f1f5f9">
        {Math.round(value)}%
      </text>
      <text x="100" y="115" textAnchor="middle" fontSize="12" fill="#94a3b8">
        Churn Risk
      </text>
    </svg>
  );
};

export default GaugeChart;
