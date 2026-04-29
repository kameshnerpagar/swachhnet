import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { useTheme } from '../context/ThemeContext';
import api from '../utils/api';

const IconSpinner = () => (
  <svg className="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
  </svg>
);

export default function CentralDashboard() {
  const { isDark } = useTheme();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get('/central/dashboard');
        setData(res.data.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen">
        <Navbar />
        <div className="flex justify-center items-center h-[60vh] text-brand-500">
          <IconSpinner />
        </div>
      </div>
    );
  }

  if (!data) return null;

  const { systemMetrics, authorities, breachedComplaints } = data;

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-8">
          <p className="text-sm font-bold mb-1 text-red-500 uppercase tracking-widest font-mono">
            System Oversight
          </p>
          <h1 className="font-display text-4xl font-bold page-title">Central Authority Dashboard</h1>
          <p className="page-subtitle mt-1 text-sm">
            Live overview of all municipal wards, resolution times, and SLA breaches.
          </p>
        </div>

        {/* Top KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <div className={`p-5 rounded-2xl border ${isDark ? 'bg-dark-800 border-gray-700' : 'bg-white border-gray-100 shadow-sm'}`}>
            <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-1">Total Wards</p>
            <p className="text-3xl font-display font-bold text-brand-500">{systemMetrics.totalWards}</p>
          </div>
          <div className={`p-5 rounded-2xl border ${isDark ? 'bg-dark-800 border-gray-700' : 'bg-white border-gray-100 shadow-sm'}`}>
            <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-1">Total Complaints</p>
            <p className="text-3xl font-display font-bold text-brand-500">{systemMetrics.totalComplaints}</p>
          </div>
          <div className={`p-5 rounded-2xl border ${isDark ? 'bg-dark-800 border-gray-700' : 'bg-white border-gray-100 shadow-sm'}`}>
            <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-1">Avg Resolution</p>
            <p className="text-3xl font-display font-bold text-green-500">{systemMetrics.avgResolutionHours}h</p>
          </div>
          <div className={`p-5 rounded-2xl border ${isDark ? 'bg-dark-800 border-red-500/30' : 'bg-red-50 border-red-200 shadow-sm'}`}>
            <p className="text-xs text-red-500 font-bold uppercase tracking-wider mb-1">Active Breaches</p>
            <p className="text-3xl font-display font-bold text-red-600">{systemMetrics.totalBreaches}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Col: Wards Leaderboard */}
          <div>
            <h2 className="text-xl font-display font-bold mb-4 flex items-center gap-2">
              <span className={isDark ? 'text-gray-100' : 'text-gray-800'}>Ward Performance</span>
            </h2>
            <div className={`rounded-2xl border overflow-hidden ${isDark ? 'border-gray-700 bg-dark-800' : 'border-gray-200 bg-white'}`}>
              <table className="w-full text-left text-sm">
                <thead className={isDark ? 'bg-dark-900/50 text-gray-400' : 'bg-gray-50 text-gray-600'}>
                  <tr>
                    <th className="px-4 py-3 font-semibold">Ward Name</th>
                    <th className="px-4 py-3 font-semibold text-center">Resolved</th>
                    <th className="px-4 py-3 font-semibold text-center">Breaches</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {authorities.sort((a, b) => b.metrics.totalResolved - a.metrics.totalResolved).map(auth => (
                    <tr key={auth._id} className="transition-colors hover:bg-gray-50 dark:hover:bg-dark-700/50">
                      <td className="px-4 py-3">
                        <p className={`font-semibold ${isDark ? 'text-gray-200' : 'text-gray-800'}`}>{auth.authorityDetails?.name || auth.name}</p>
                        <p className="text-xs text-gray-500">{auth.email}</p>
                      </td>
                      <td className="px-4 py-3 text-center font-mono font-bold text-green-600 dark:text-green-400">
                        {auth.metrics.totalResolved}
                      </td>
                      <td className="px-4 py-3 text-center">
                        {auth.metrics.activeBreaches > 0 ? (
                          <span className="inline-block bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 px-2 py-1 rounded font-bold text-xs animate-pulse">
                            {auth.metrics.activeBreaches}
                          </span>
                        ) : (
                          <span className="text-gray-400">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Right Col: Active Breaches Feed */}
          <div>
            <h2 className="text-xl font-display font-bold mb-4 flex items-center gap-2">
              <span className="text-red-500">⚠️ Active SLA Breaches (48h+)</span>
            </h2>
            
            <div className="space-y-3">
              {breachedComplaints.length === 0 ? (
                <div className={`p-8 text-center rounded-2xl border ${isDark ? 'bg-dark-800 border-gray-700' : 'bg-white border-gray-200'}`}>
                  <p className="text-green-500 font-bold text-lg mb-1">All clear!</p>
                  <p className="text-gray-500 text-sm">No wards are currently breaching the 48-hour SLA.</p>
                </div>
              ) : (
                breachedComplaints.map(complaint => (
                  <div key={complaint._id} className={`p-4 rounded-xl border-l-4 border-l-red-500 border-y border-r flex gap-4 ${isDark ? 'bg-dark-800 border-gray-700' : 'bg-white border-gray-200 shadow-sm'}`}>
                    <img 
                      src={complaint.imageUrl} 
                      alt="Garbage" 
                      className="w-24 h-24 object-cover rounded-lg flex-shrink-0 bg-gray-200"
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400 uppercase tracking-wider">
                          Breached
                        </span>
                        <span className="text-xs text-gray-500 font-mono">
                          {new Date(complaint.createdAt).toLocaleDateString()}
                        </span>
                      </div>
                      <p className={`font-semibold text-sm truncate ${isDark ? 'text-gray-200' : 'text-gray-800'}`}>
                        {complaint.location?.address || 'Unknown Location'}
                      </p>
                      <p className="text-xs text-gray-500 mb-2 mt-0.5 truncate">
                        Assigned to: <strong className={isDark ? 'text-gray-300' : 'text-gray-700'}>{complaint.authorityId?.authorityDetails?.name || complaint.authorityId?.name}</strong>
                      </p>
                      <div className="text-xs text-gray-400 bg-gray-50 dark:bg-dark-900 px-2 py-1.5 rounded truncate">
                        {complaint.description || 'No description provided.'}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
