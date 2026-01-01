export interface ChatResponse {
    action: 'reply' | 'escalate';
    text: string;
    report?: any;
}

export interface Issue {
    id: number;
    description: string;
    department: string;
    priority: string;
    status: string;
    ai_summary?: string;
    assigned_to?: number;
    created_at: string;
}

export const API = {
    async sendMessage(message: string, userId: string = "guest"): Promise<ChatResponse> {
        const baseUrl = import.meta.env.VITE_API_URL || '/api'; // Use env var in prod, proxy in dev

        // Remove trailing slash if exists to avoid double slash
        const url = `${baseUrl.replace(/\/$/, '')}/chat`;

        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, user_id: userId })
        });
        if (!res.ok) throw new Error('Network error');
        return res.json();
    },

    async getIssues(): Promise<Issue[]> {
        const res = await fetch('/api/issues');
        if (!res.ok) throw new Error('Network error');
        return res.json();
    }
};
