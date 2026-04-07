import React, { useState, useEffect } from 'react';
import { Activity, Zap, AlertTriangle, TrendingUp, CheckCircle } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import GaugeChart from './components/GaugeChart';
import InputMatrix from './components/InputMatrix';
import ModelStatus from './components/ModelStatus';
import ActionCard from './components/ActionCard';

export default function App() {
  const [churnProb, setChurnProb] = useState(42);
  const [riskLevel, setRiskLevel] = useState('Medium');
  const [inputs, setInputs] = useState({});
  const [loading, setLoading] = useState(false);

  const getRiskColor = (prob) => {
    if (prob < 33) return { bg: 'bg-emerald-500', text: 'text-emerald-400', label: 'Low Risk', badge: 'bg-emerald-500/20 border-emerald-500/50', level: 'low' };
    if (prob < 66) return { bg: 'bg-amber-500', text: 'text-amber-400', label: 'Medium Risk', badge: 'bg-amber-500/20 border-amber-500/50', level: 'medium' };
    return { bg: 'bg-red-500', text: 'text-red-400', label: 'Critical Risk', badge: 'bg-red-500/20 border-red-500/50', level: 'high' };
  };

  const risk = getRiskColor(churnProb);
  const topFeatures = [
    { name: 'Satisfaction Score', value: 28, color: 'from-indigo-500 to-cyan-400' },
    { name: 'Days Since Last Order', value: 22, color: 'from-violet-500 to-indigo-400' },
    { name: 'Cashback Amount', value: 15, color: 'from-cyan-400 to-blue-500' },
  ];

  const handlePredict = async () => {
    setLoading(true);
    setTimeout(() => {
      setChurnProb(Math.floor(Math.random() * 100));
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-white font-sans overflow-x-hidden">
      {/* Animated Background Gradient */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl"></div>
      </div>

      {/* Main Container */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8">
        
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-cyan-400 to-violet-400 mb-2">
            Churn Prediction Engine
          </h1>
          <p className="text-gray-400 text-lg">AI-Powered E-commerce Customer Retention</p>
        </div>

        {/* Top Section: Status + Gauge */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          
          {/* Model Status */}
          <ModelStatus />

          {/* Gauge */}
          <div className="lg:col-span-2 backdrop-blur-md bg-slate-900/40 border border-indigo-500/20 rounded-3xl p-8 hover:scale-[1.02] transition-transform duration-300 shadow-glow">
            <div className="flex flex-col items-center justify-center h-80">
              <GaugeChart value={churnProb} />
              <div className={`mt-6 px-6 py-3 rounded-full border ${risk.badge} flex items-center gap-2`}>
                <span className={`inline-block w-3 h-3 rounded-full ${risk.bg} animate-pulse`}></span>
                <span className={`font-semibold text-lg ${risk.text}`}>{risk.label}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Input Matrix */}
        <InputMatrix onInputChange={setInputs} onPredict={handlePredict} loading={loading} />

        {/* Impact Zone */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          
          {/* Feature Importance */}
          <div className="lg:col-span-2 backdrop-blur-md bg-slate-900/40 border border-indigo-500/20 rounded-3xl p-8">
            <h3 className="text-2xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400">
              Feature Impact
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topFeatures}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.3)' }} />
                <Bar dataKey="value" radius={[0, 12, 12, 0]} fill="url(#gradient)">
                  <defs>
                    <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#818cf8" />
                      <stop offset="100%" stopColor="#22d3ee" />
                    </linearGradient>
                  </defs>
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Action Card */}
          <ActionCard churnProbability={churnProb / 100} riskLevel={risk.level} />
        </div>
      </div>
    </div>
  );
}
