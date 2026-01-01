import { Bot, User } from 'lucide-react';
import { cn } from '../../lib/utils';
import type { ChatMessage } from '../../types';
import { AIResponseCard } from './AIResponseCard';

interface MessageBubbleProps {
    message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
    const isAI = message.sender === 'ai';

    return (
        <div className={cn(
            "flex w-full mb-8 animate-in fade-in duration-300",
            isAI ? "justify-start" : "justify-end"
        )}>
            <div className={cn(
                "flex max-w-[85%] md:max-w-[75%]",
                isAI ? "flex-row" : "flex-row-reverse"
            )}>
                {/* Avatar */}
                <div className={cn(
                    "flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center border-2 border-white shadow-sm mt-1",
                    isAI ? "bg-gradient-to-br from-brand-primary to-brand-role-ai text-white mr-4" : "bg-slate-200 text-slate-500 ml-4"
                )}>
                    {isAI ? <Bot size={20} /> : <User size={20} />}
                </div>

                {/* Content */}
                <div className="flex flex-col">
                    <div className={cn(
                        "p-4 rounded-2xl shadow-sm leading-relaxed text-sm lg:text-base",
                        isAI
                            ? "bg-white text-brand-text-body border border-slate-100 rounded-tl-none"
                            : "bg-brand-primary text-white rounded-tr-none"
                    )}>
                        {message.text}

                        {/* Visual Logic Indicators */}
                        {isAI && !message.text.includes("trouble connecting") && (
                            <div className="mt-2 flex gap-2 text-[10px] uppercase font-bold tracking-wider opacity-70 border-t border-slate-100 pt-2">
                                {(message.structuredData || message.text.includes("forwarding this")) ? (
                                    <span className="text-amber-600 flex items-center gap-1">
                                        🚨 Escalated
                                    </span>
                                ) : (
                                    <span className="text-emerald-600 flex items-center gap-1">
                                        🤖 AI Auto-Reply
                                    </span>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Structured Data Attachment */}
                    {isAI && message.structuredData && (
                        <AIResponseCard data={message.structuredData} />
                    )}

                    <span className={cn(
                        "text-[10px] text-slate-400 mt-2",
                        isAI ? "text-left ml-1" : "text-right mr-1"
                    )}>
                        {message.timestamp}
                    </span>
                </div>
            </div>
        </div>
    );
}
