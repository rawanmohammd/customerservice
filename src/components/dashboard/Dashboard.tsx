import { useMockApp } from '../../lib/store';
import { ReportCard } from './ReportCard';
import { CheckCircle2, TrendingUp, AlertCircle, Clock } from 'lucide-react';
import { API } from '../../lib/api';
import { useState, useEffect } from 'react';

export function Dashboard() {
    const { reports, currentUser } = useMockApp();
    const [liveReports, setLiveReports] = useState<any[]>([]);

    useEffect(() => {
        const fetchIssues = async () => {
            try {
                const issues = await API.getIssues();
                const mapped = issues.map(i => ({
                    id: i.id.toString(),
                    clientId: "Client #" + (i.assigned_to || "?"),
                    summary: i.description,
                    department: i.department,
                    status: i.status,
                    priority: i.priority,
                    createdAt: new Date(i.created_at),
                    tags: ["API"]
                }));
                // Only update if we have data to show "Live" feel
                if (mapped.length > 0) setLiveReports(mapped.reverse());
            } catch (e) { console.error(e); }
        };
        fetchIssues(); // Initial
        const timer = setInterval(fetchIssues, 3000); // Poll
        return () => clearInterval(timer);
    }, []);

    // Merge live reports with mock reports for the demo
    const displayReports = [...liveReports, ...reports];

    const stats = [
        { label: 'Pending Requests', value: displayReports.length.toString(), icon: <Clock size={20} />, color: 'text-orange-500 bg-orange-50' },
        { label: 'Active Projects', value: '8', icon: <TrendingUp size={20} />, color: 'text-blue-500 bg-blue-50' },
        { label: 'Completed', value: '128', icon: <CheckCircle2 size={20} />, color: 'text-green-500 bg-green-50' },
        { label: 'Urgent Actions', value: displayReports.filter(r => r.priority === 'high').length.toString(), icon: <AlertCircle size={20} />, color: 'text-red-500 bg-red-50' },
    ];

    return (
        <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">

            {/* Welcome Section */}
            <div>
                <h1 className="text-2xl font-bold text-brand-text-heading">Welcome back, {currentUser.name.split(' ')[0]}</h1>
                <p className="text-brand-text-muted">Here is what's happening in the {currentUser.department?.toUpperCase() || 'Company'} today.</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {stats.map((stat, i) => (
                    <div key={i} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
                        <div className={`p-3 rounded-lg ${stat.color}`}>
                            {stat.icon}
                        </div>
                        <div>
                            <div className="text-2xl font-bold text-brand-text-heading">{stat.value}</div>
                            <div className="text-xs text-brand-text-muted font-medium">{stat.label}</div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Reports Section */}
            <div>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-brand-text-heading">Recent AI Reports</h2>
                    <button className="text-sm text-brand-primary font-medium hover:underline">View All</button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {displayReports.map((report) => (
                        <ReportCard key={report.id} report={report} />
                    ))}

                    {/* Add Mock cards if few */}
                    {reports.length < 5 && [1, 2].map((i) => (
                        <div key={i} className="border-2 border-dashed border-slate-200 rounded-xl p-6 flex flex-col items-center justify-center text-slate-400 min-h-[200px]">
                            <span className="text-sm">Waiting for new requests...</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
