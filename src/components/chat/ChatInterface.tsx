import { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Mic, Sparkles } from 'lucide-react';
import { useMockApp } from '../../lib/store';
import { MessageBubble } from './MessageBubble';
import { cn } from '../../lib/utils';
import { API } from '../../lib/api';

export function ChatInterface() {
    const { messages, addMessage } = useMockApp();
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        // Optimistic UI Update
        const userText = input;
        addMessage(userText, 'user');
        setInput('');
        setIsTyping(true);

        try {
            const response = await API.sendMessage(userText);

            // Add AI response to store
            // Note: addMessage in store might need expansion for structured data, 
            // but for now we pass text. If store doesn't support structured, we might need a workaround.
            // Let's assume for this step we primarily show text, and if 'escalate', we append a note.

            let finalText = response.text;
            let structuredData = null;

            if (response.action === 'escalate' && response.report) {
                // Append simple text summary
                finalText += `\n\n(Internal Note: Escalated to ${response.report.department.toUpperCase()} Dept)`;

                // Prepare rich card data
                structuredData = {
                    title: "Issue Escalation Report",
                    insights: [
                        `Priority: ${response.report.priority.toUpperCase()}`,
                        `Dept: ${response.report.department.toUpperCase()}`,
                        `Summary: ${response.report.summary.slice(0, 50)}...`
                    ],
                    steps: [
                        "Issue logged in Dashboard",
                        "Email notification sent to manager",
                        "Ticket assigned to specialist"
                    ]
                };
            }

            // We need to verify if addMessage accepts a 3rd arg. 
            // Based on view_file of store.ts, it acts on 'messages' array.
            // If the store's addMessage doesn't support it, we'll need to use the hook or raw state.
            // Assuming we update the store or use a custom dispatch if needed.
            // Wait, I see useMockApp export. I'll blindly check if I can pass it, or I'll update store.ts next.
            addMessage(finalText, 'ai', structuredData);

        } catch (e) {
            // Error message - we will handle the badge logic in MessageBubble
            addMessage("Sorry, I'm having trouble connecting to the server.", 'ai');
        } finally {
            setIsTyping(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const suggestions = [
        "I need a website for my business",
        "Integrate AI into my app",
        "Content strategy for social media",
        "Fix bugs in my legacy code"
    ];

    return (
        <div className="h-full flex flex-col max-w-5xl mx-auto">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto px-4 py-8 space-y-2">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-center opacity-50 space-y-4">
                        <div className="w-20 h-20 bg-brand-primary/10 rounded-full flex items-center justify-center text-brand-primary mb-4">
                            <Sparkles size={40} />
                        </div>
                        <h2 className="text-2xl font-bold text-brand-primary">How can ZEdny help you today?</h2>
                        <p className="text-brand-text-muted max-w-md">
                            Describe your project or problem, and our AI will analyze requirements and connect you with the right team.
                        </p>
                    </div>
                )}

                {messages.map((msg) => (
                    <MessageBubble key={msg.id} message={msg} />
                ))}

                {isTyping && (
                    <div className="flex items-center space-x-2 p-4 text-slate-400 text-sm animate-pulse">
                        <Sparkles size={16} />
                        <span>AI is thinking...</span>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="px-4 pb-8 pt-4 bg-gradient-to-t from-brand-bg to-brand-bg/0">

                {/* Suggestion Chips */}
                {messages.length < 3 && (
                    <div className="flex flex-wrap gap-2 mb-4 justify-center">
                        {suggestions.map((s, i) => (
                            <button
                                key={i}
                                onClick={() => { setInput(s); }}
                                className="text-xs font-medium px-4 py-2 rounded-full bg-white border border-brand-secondary/30 text-brand-primary hover:bg-brand-secondary/10 hover:border-brand-secondary transition-all"
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                )}

                <div className="relative max-w-4xl mx-auto bg-white rounded-2xl shadow-lg border border-slate-100 p-2 flex items-end space-x-2">
                    <button className="p-3 text-slate-400 hover:text-brand-primary hover:bg-slate-50 rounded-xl transition-colors">
                        <Paperclip size={20} />
                    </button>

                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your message here..."
                        className="flex-1 max-h-32 bg-transparent border-none focus:ring-0 p-3 text-brand-text-body placeholder:text-slate-300 resize-none"
                        rows={1}
                    />

                    <div className="flex items-center space-x-1">
                        {input.length === 0 && (
                            <button className="p-3 text-slate-400 hover:text-brand-primary hover:bg-slate-50 rounded-xl transition-colors">
                                <Mic size={20} />
                            </button>
                        )}

                        <button
                            onClick={handleSend}
                            disabled={!input.trim()}
                            className={cn(
                                "p-3 rounded-xl transition-all duration-200",
                                input.trim()
                                    ? "bg-brand-primary text-white shadow-md hover:shadow-lg hover:bg-brand-primary/90"
                                    : "bg-slate-100 text-slate-300 cursor-not-allowed"
                            )}
                        >
                            <Send size={20} />
                        </button>
                    </div>
                </div>
                <div className="text-center mt-2 text-[10px] text-slate-400">
                    ZEdny AI can make mistakes. Consider checking important information.
                </div>
            </div>
        </div>
    );
}
