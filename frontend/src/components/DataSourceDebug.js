import { useState, useEffect } from 'react';

const DataSourceDebug = ({ dataSource, apiUrl, error }) => {
  const [isVisible, setIsVisible] = useState(true);

  // Auto-hide after 10 seconds
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(false), 10000);
    return () => clearTimeout(timer);
  }, []);

  if (!isVisible) return null;

  return (
    <div className="fixed top-4 right-4 bg-slate-900 text-white p-4 rounded-lg shadow-lg z-50 max-w-sm">
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-bold text-sm">Debug Info</h4>
        <button 
          onClick={() => setIsVisible(false)}
          className="text-slate-400 hover:text-white"
        >
          ×
        </button>
      </div>
      
      <div className="space-y-2 text-xs">
        <div>
          <span className="text-slate-400">Data Source:</span>
          <span className={`ml-2 px-2 py-1 rounded ${
            dataSource === 'API' ? 'bg-green-600' : 'bg-orange-600'
          }`}>
            {dataSource || 'Unknown'}
          </span>
        </div>
        
        <div>
          <span className="text-slate-400">API URL:</span>
          <div className="text-slate-300 break-all">{apiUrl}</div>
        </div>
        
        {error && (
          <div>
            <span className="text-slate-400">Error:</span>
            <div className="text-red-400 text-xs">{error}</div>
          </div>
        )}
        
        <div className="text-slate-500 text-xs mt-2">
          {dataSource === 'API' ? '✅ Using real backend data' : '⚠️ Using fallback mock data'}
        </div>
      </div>
    </div>
  );
};

export default DataSourceDebug;