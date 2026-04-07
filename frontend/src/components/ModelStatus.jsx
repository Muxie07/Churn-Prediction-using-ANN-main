import React, { useState, useEffect } from 'react';
import { CheckCircle, Zap } from 'lucide-react';

const ModelStatus = ({ latency = 24, modelVersion = 'CatBoost-v4', status = 'Online' }) => {
  const [isOnline, setIsOnline] = useState(status === 'Online');

  useEffect(() => {
    // Simulate latency fluctuation
    const interval = setInterval(() => {
      setIsOnline(Math.random() > 0.05); // 95% online
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="backdrop-blur-md bg-gradient-to-br from-slate-900/50 to-slate-800/30 border border-indigo-500/20 rounded-3xl p-6 shadow-glow">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-100 mb-1">Model Status</h3>
          <p className="text-xs text-gray-400">Live inference metrics</p>
        </div>
        <div className="relative">
          <div
            className={`w-3 h-3 rounded-full ${
              isOnline ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'
            }`}
          />
          <div
            className={`absolute inset-0 w-3 h-3 rounded-full ${
              isOnline ? 'bg-emerald-400/30 animate-pulse' : ''
            }`}
          />
        </div>
      </div>

      <div className="space-y-4">
        {/* Latency */}
        <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-indigo-500/10 hover:border-indigo-500/30 transition-colors">
          <div className="flex items-center gap-2">
            <Zap size={16} className="text-cyan-400" />
            <span className="text-sm text-gray-300">Latency</span>
          </div>
          <span className="text-sm font-mono font-bold text-cyan-400">{latency}ms</span>
        </div>

        {/* Model Version */}
        <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-indigo-500/10 hover:border-indigo-500/30 transition-colors">
          <div className="flex items-center gap-2">
            <CheckCircle size={16} className="text-indigo-400" />
            <span className="text-sm text-gray-300">Model</span>
          </div>
          <span className="text-sm font-mono text-indigo-400">{modelVersion}</span>
        </div>

        {/* Status */}
        <div className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl border border-indigo-500/10 hover:border-indigo-500/30 transition-colors">
          <span className="text-sm text-gray-300">Status</span>
          <span className={`text-sm font-bold ${isOnline ? 'text-emerald-400' : 'text-red-400'}`}>
            {isOnline ? '🟢 Online' : '🔴 Offline'}
          </span>
        </div>
      </div>

      {/* Performance Indicator */}
      <div className="mt-4 pt-4 border-t border-indigo-500/10">
        <div className="text-xs text-gray-400 mb-2">Model Confidence</div>
        <div className="w-full h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400"
            style={{ width: '94%' }}
          />
        </div>
        <div className="text-xs text-gray-400 mt-1 text-right">94%</div>
      </div>
    </div>
  );
};

export default ModelStatus;
