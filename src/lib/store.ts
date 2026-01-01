import { useState } from 'react';
import type { User, ChatMessage, Report, UserRole } from '../types';

// Mock Data
const MOCK_USERS: Record<UserRole, User> = {
    client: {
        id: 'u1',
        name: 'Sarah Miller',
        avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150',
        role: 'client'
    },
    employee: {
        id: 'e1',
        name: 'Alex Chen',
        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=150',
        role: 'employee',
        department: 'ai'
    },
    admin: {
        id: 'a1',
        name: 'Jordan Boss',
        avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=150',
        role: 'admin'
    }
};

export const INITIAL_MESSAGES: ChatMessage[] = [
    {
        id: '1',
        sender: 'ai',
        text: 'Hello! I am ZEdny AI. How can I assist you with your software needs today?',
        timestamp: '10:00 AM'
    }
];

export const MOCK_REPORTS: Report[] = [
    {
        id: 'r1',
        clientName: 'TechCorp Industries',
        summary: 'Custom AI Model Training for Logistics',
        department: 'ai',
        priority: 'high',
        status: 'new',
        createdAt: '2 mins ago'
    },
    {
        id: 'r2',
        clientName: 'GreenLeaf Cafe',
        summary: 'E-commerce Website Overhaul',
        department: 'web',
        priority: 'medium',
        status: 'in-progress',
        createdAt: '1 hour ago'
    },
    {
        id: 'r3',
        clientName: 'StartupX',
        summary: 'SEO & Content Strategy for Launch',
        department: 'content',
        priority: 'low',
        status: 'new',
        createdAt: '3 hours ago'
    }
];

// Simple State Hook
export function useMockApp() {
    const [showLanding, setShowLanding] = useState(true);
    const [currentUser, setCurrentUser] = useState<User>(MOCK_USERS.client);
    const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
    const [reports] = useState<Report[]>(MOCK_REPORTS);

    const matchRole = (role: UserRole) => {
        setCurrentUser(MOCK_USERS[role]);
        setShowLanding(false);
    };

    const switchRole = (role: UserRole) => {
        setCurrentUser(MOCK_USERS[role]);
    };

    const addMessage = (text: string, sender: 'user' | 'ai', structuredData?: any) => {
        const newMsg: ChatMessage = {
            id: Date.now().toString(),
            sender,
            text,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            structuredData
        };
        setMessages(prev => [...prev, newMsg]);
    };

    return {
        currentUser,
        messages,
        reports,
        showLanding,
        matchRole,
        switchRole,
        addMessage
    };
}
