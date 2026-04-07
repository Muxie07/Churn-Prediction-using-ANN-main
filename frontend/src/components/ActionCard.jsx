import React from 'react';
import { AlertCircle, TrendingDown, Lightbulb } from 'lucide-react';

const ActionCard = ({ churnProbability = 0.45, riskLevel = 'medium' }) => {
  const isHighRisk = churnProbability > 0.7;
  const isMediumRisk = churnProbability > 0.4 && churnProbability <= 0.7;

  const recommendations = {
    low: {
      icon: '✨',
      title: 'Customer Retention Strong',
      action: 'Monitor engagement metrics quarterly',
      color: 'from-emerald-500/80 to-teal-600/60',
      border: 'border-emerald-500/30',
      glow: 'shadow-lg',
    },
    medium: {
      icon: '⚠️',
      title: 'Engagement Improvement Needed',
      action: 'Offer personalized discounts or new product recommendations',
      color: 'from-amber-500/80 to-orange-600/60',
      border: 'border-amber-500/30',
      glow: 'shadow-glow-orange',
    },
    high: {
      icon: '🚨',
      title: 'Critical Retention Alert',
      action: 'Immediate intervention: Priority customer support + exclusive retention offer',
      color: 'from-red-500/80 to-rose-600/60',
      border: 'border-red-500/30',
      glow: 'shadow-glow-red',
    },
  };

  const config = recommendations[riskLevel] || recommendations.low;

  return (
    <div
      className={`backdrop-blur-md bg-gradient-to-br ${config.color} border ${config.border} rounded-3xl p-6 ${config.glow} transition-all duration-300`}
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div className="text-4xl flex-shrink-0">{config.icon}</div>

        {/* Content */}
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white mb-2">{config.title}</h3>
          <p className="text-sm text-gray-100 mb-4 leading-relaxed">{config.action}</p>

          {/* Action Buttons */}
          <div className="flex gap-3 flex-wrap">
            <button className="text-xs px-4 py-2 rounded-lg bg-white/20 hover:bg-white/30 text-white font-medium transition-all border border-white/20 hover:border-white/40">
              View Details
            </button>
            {isHighRisk && (
              <button className="text-xs px-4 py-2 rounded-lg bg-white/80 hover:bg-white text-slate-900 font-bold transition-all">
                Send Offer
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Risk Probability Bar */}
      <div className="mt-4 pt-4 border-t border-white/10">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-white/80">Churn Probability</span>
          <span className="text-sm font-bold text-white">{Math.round(churnProbability * 100)}%</span>
        </div>
        <div className="w-full h-2 bg-white/20 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-emerald-400 via-amber-400 to-red-500 transition-all duration-500"
            style={{ width: `${churnProbability * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default ActionCard;
