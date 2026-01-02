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

// Helper to get base URL
const getBaseUrl = () => {
    const url = import.meta.env.VITE_API_URL || '/api';
    return url.replace(/\/$/, ''); // Remove trailing slash
};

export const API = {
    async sendMessage(message: string, sessionId: string = "default"): Promise<ChatResponse> {
        // FastAPI expects trailing slash by default -> /chat/
        const url = `${getBaseUrl()}/chat/`;

        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: sessionId })
        });

        // Handle 307 Redirects explicitly if fetch doesn't
        if (res.status === 307) {
            const newUrl = res.headers.get('Location');
            if (newUrl) {
                return (await fetch(newUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, session_id: sessionId })
                })).json();
            }
        }

        if (!res.ok) throw new Error(`Network error: ${res.status}`);
        return res.json();
    },

    async getIssues(): Promise<Issue[]> {
        try {
            // FastAPI expects trailing slash -> /issues/
            const url = `${getBaseUrl()}/issues/`;

            const res = await fetch(url);
            if (!res.ok) return []; // Return empty array on error

            const data = await res.json();
            return Array.isArray(data) ? data : []; // Verify it's an array
        } catch (e) {
            console.error("Failed to fetch issues:", e);
            return []; // Safe fallback
        }
    }
};
