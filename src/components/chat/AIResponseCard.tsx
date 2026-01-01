import { ArrowRight, CheckCircle2, FileText, Layers } from 'lucide-react';


export interface AIResponseProps {
    data: {
        title: string;
        points: string[];
        steps: string[];
    };
}

export function AIResponseCard({ data }: AIResponseProps) {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-brand-secondary/20 overflow-hidden mt-2 max-w-2xl animate-in fade-in slide-in-from-bottom-2 duration-500">
            <div className="bg-brand-secondary/5 px-6 py-4 border-b border-brand-secondary/10 flex items-center space-x-3">
                <div className="p-2 bg-white rounded-lg shadow-sm text-brand-secondary">
                    <Layers size={20} />
                </div>
                <h3 className="font-semibold text-brand-primary">{data.title}</h3>
            </div>

            <div className="p-6 space-y-6">
                <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-xs font-semibold text-brand-text-muted uppercase tracking-wider">
                        <FileText size={14} />
                        <span>Key Insights</span>
                    </div>
                    <ul className="space-y-2">
                        {data.points.map((point, idx) => (
                            <li key={idx} className="flex items-start space-x-3 text-sm text-brand-text-body">
                                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-brand-secondary flex-shrink-0" />
                                <span>{point}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-xs font-semibold text-brand-text-muted uppercase tracking-wider">
                        <ArrowRight size={14} />
                        <span>Recommended Steps</span>
                    </div>
                    <div className="grid gap-3">
                        {data.steps.map((step, idx) => (
                            <div key={idx} className="group flex items-center justify-between p-3 rounded-lg border border-slate-100 hover:border-brand-secondary/30 hover:bg-brand-secondary/5 transition-all cursor-pointer">
                                <div className="flex items-center space-x-3">
                                    <div className="w-6 h-6 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center text-xs font-medium group-hover:bg-brand-secondary group-hover:text-white transition-colors">
                                        {idx + 1}
                                    </div>
                                    <span className="text-sm font-medium text-brand-text-heading">{step}</span>
                                </div>
                                <CheckCircle2 size={16} className="text-slate-300 group-hover:text-brand-secondary transition-colors opacity-0 group-hover:opacity-100" />
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 text-xs text-center text-slate-400">
                AI Generated Report • ZEdny Intelligence
            </div>
        </div>
    );
}
