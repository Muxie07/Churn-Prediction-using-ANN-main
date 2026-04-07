import React from 'react';
import { Zap } from 'lucide-react';

const InputMatrix = ({ onInputChange, onPredict, loading }) => {
  const categories = {
    Demographics: [
      { label: 'Age', type: 'range', min: 18, max: 80, default: 35 },
      { label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other'], default: 'Male' },
      { label: 'City Tier', type: 'select', options: ['Tier 1', 'Tier 2', 'Tier 3'], default: 'Tier 1' },
    ],
    Account: [
      { label: 'Tenure (months)', type: 'range', min: 0, max: 240, default: 72 },
      { label: 'Preferred Device', type: 'select', options: ['Desktop', 'Mobile', 'Tablet'], default: 'Mobile' },
      { label: 'Warehouse Distance', type: 'range', min: 0, max: 100, default: 50 },
    ],
    Behavioral: [
      { label: 'Satisfaction', type: 'range', min: 1, max: 5, default: 3 },
      { label: 'Order Category', type: 'select', options: ['Electronics', 'Fashion', 'Grocery'], default: 'Electronics' },
      { label: 'Addresses', type: 'range', min: 1, max: 10, default: 3 },
    ],
    Financial: [
      { label: 'Order Amount Hike (%)', type: 'range', min: 0, max: 100, default: 15 },
      { label: 'Coupon Used', type: 'select', options: ['Yes', 'No'], default: 'No' },
      { label: 'Days Since Last Order', type: 'range', min: 0, max: 365, default: 30 },
      { label: 'Cashback Amount', type: 'range', min: 0, max: 5000, default: 500 },
    ],
  };

  return (
    <div className="space-y-8 mb-8">
      {Object.entries(categories).map(([category, fields]) => (
        <div key={category}>
          <h3 className="text-xl font-semibold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
            {category}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {fields.map((field, idx) => (
              <div
                key={idx}
                className="backdrop-blur-md bg-slate-900/40 border border-indigo-500/20 rounded-2xl p-4 hover:scale-[1.02] hover:border-indigo-500/40 transition-all duration-300 cursor-pointer"
              >
                <label className="text-sm font-medium text-gray-300 block mb-2">{field.label}</label>
                {field.type === 'range' ? (
                  <input
                    type="range"
                    min={field.min}
                    max={field.max}
                    defaultValue={field.default}
                    className="w-full h-1 bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                  />
                ) : (
                  <select className="w-full bg-slate-800/50 border border-indigo-500/30 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500/60">
                    {field.options.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* Predict Button */}
      <button
        onClick={onPredict}
        disabled={loading}
        className="w-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-violet-500 hover:from-indigo-600 hover:to-violet-600 disabled:opacity-50 text-white font-bold py-4 rounded-2xl transition-all duration-300 flex items-center justify-center gap-2 shadow-glow hover:shadow-lg"
      >
        <Zap size={20} />
        {loading ? 'Analyzing...' : 'Run Prediction'}
      </button>
    </div>
  );
};

export default InputMatrix;
