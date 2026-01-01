import type { Report, Department } from '../../types';
import { cn } from '../../lib/utils';
import { MoreHorizontal, Clock, ArrowRight } from 'lucide-react';

interface ReportCardProps {
    report: Report;
}

const deptColors: Record<Department, string> = {
    web: 'text-brand-role-web bg-brand-role-web/10 border-brand-role-web/20',
    ai: 'text-brand-role-ai bg-brand-role-ai/10 border-brand-role-ai/20',
    content: 'text-brand-role-content bg-brand-role-content/10 border-brand-role-content/20',
};

const priorityConfig = {
    low: 'bg-slate-100 text-slate-600',
    medium: 'bg-orange-100 text-orange-600',
    high: 'bg-red-100 text-red-600',
};

export function ReportCard({ report }: ReportCardProps) {
    return (
        <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-shadow group">
            <div className="flex justify-between items-start mb-4">
                <div className={cn(
                    "px-2.5 py-1 rounded-md text-xs font-semibold uppercase tracking-wider border",
                    deptColors[report.department]
                )}>
                    {report.department}
                </div>
                <button className="text-slate-400 hover:text-brand-primary">
                    <MoreHorizontal size={16} />
                </button>
            </div>

            <h3 className="font-semibold text-brand-text-heading mb-2 group-hover:text-brand-primary transition-colors">
                {report.summary}
            </h3>

            <p className="text-sm text-brand-text-muted mb-4">
                Client: <span className="text-brand-text-body font-medium">{report.clientName}</span>
            </p>

            <div className="flex items-center justify-between pt-4 border-t border-slate-50">
                <div className="flex items-center space-x-2">
                    <span className={cn("text-[10px] font-bold px-2 py-0.5 rounded-full uppercase", priorityConfig[report.priority])}>
                        {report.priority}
                    </span>
                    <div className="flex items-center text-xs text-slate-400">
                        <Clock size={12} className="mr-1" />
                        {report.createdAt}
                    </div>
                </div>

                <button className="text-brand-primary opacity-0 group-hover:opacity-100 transition-opacity transform translate-x-[-10px] group-hover:translate-x-0 duration-300">
                    <ArrowRight size={18} />
                </button>
            </div>
        </div>
    );
}
