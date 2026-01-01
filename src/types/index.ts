export type UserRole = 'client' | 'employee' | 'admin';
export type Department = 'web' | 'ai' | 'content';

export interface User {
    id: string;
    name: string;
    avatar: string;
    role: UserRole;
    department?: Department;
}

export interface ChatMessage {
    id: string;
    sender: 'user' | 'ai';
    text: string;
    timestamp: string;
    structuredData?: {
        title: string;
        points: string[];
        steps: string[];
    };
}

export interface Report {
    id: string;
    clientName: string;
    summary: string;
    department: Department;
    priority: 'low' | 'medium' | 'high';
    status: 'new' | 'in-progress' | 'completed';
    createdAt: string;
}
