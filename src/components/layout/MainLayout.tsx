import React, { useState } from 'react';
import type { User, UserRole } from '../../types';
import { cn } from '../../lib/utils';
import {
    LayoutDashboard,
    MessageSquare,
    Settings,
    Bell,
    LogOut,
    Menu,
    FileCode,
    Bot,
    PenTool
} from 'lucide-react';

interface LayoutProps {
    children: React.ReactNode;
    user: User;
    onSwitchRole: (role: UserRole) => void;
}

export function Layout({ children, user, onSwitchRole }: LayoutProps) {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    return (
        <div className="min-h-screen flex bg-brand-bg transition-colors duration-300">
            {/* Sidebar - Only for Employees/Admin */}
            {user.role !== 'client' && (
                <aside
                    className={cn(
                        "fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-slate-200 transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0",
                        !sidebarOpen && "-translate-x-full lg:hidden"
                    )}
                >
                    <div className="h-full flex flex-col">
                        <div className="h-16 flex items-center px-6 border-b border-slate-100">
                            <span className="text-2xl font-bold bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
                                ZEdny
                            </span>
                        </div>

                        <nav className="flex-1 px-4 py-6 space-y-1">
                            <NavItem icon={<LayoutDashboard size={20} />} label="Dashboard" active />
                            <NavItem icon={<MessageSquare size={20} />} label="Inbox" />
                            <NavItem icon={<FileCode size={20} />} label="Projects" />

                            <div className="pt-6 pb-2 px-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                Departments
                            </div>
                            <NavItem icon={<Settings size={20} />} label="Web Dev" />
                            <NavItem icon={<Bot size={20} />} label="AI Solutions" />
                            <NavItem icon={<PenTool size={20} />} label="Content" />
                        </nav>

                        <div className="p-4 border-t border-slate-100">
                            <button className="flex items-center space-x-3 w-full px-4 py-2 text-brand-text-muted hover:text-red-500 transition-colors">
                                <LogOut size={20} />
                                <span>Logout</span>
                            </button>
                        </div>
                    </div>
                </aside>
            )}

            {/* Main Content */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Top Header */}
                <header className="h-16 bg-white/80 backdrop-blur-md border-b border-slate-100 flex items-center justify-between px-4 sm:px-6 lg:px-8 z-40 sticky top-0">
                    <div className="flex items-center">
                        {user.role !== 'client' && (
                            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="lg:hidden mr-4 text-slate-500">
                                <Menu size={24} />
                            </button>
                        )}
                        {user.role === 'client' && (
                            <span className="text-xl font-bold text-brand-primary">ZEdny Portal</span>
                        )}
                    </div>

                    <div className="flex items-center space-x-4">
                        {/* Role Switcher for Demo */}
                        <select
                            className="text-xs border border-brand-primary/20 rounded px-2 py-1 bg-transparent text-brand-primary focus:outline-none"
                            value={user.role}
                            onChange={(e) => onSwitchRole(e.target.value as UserRole)}
                        >
                            <option value="client">Client View</option>
                            <option value="employee">Employee View</option>
                            <option value="admin">Admin View</option>
                        </select>

                        <button className="relative p-2 text-slate-400 hover:text-brand-primary transition-colors">
                            <Bell size={20} />
                            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
                        </button>

                        <div className="flex items-center space-x-3 pl-4 border-l border-slate-100">
                            <div className="text-right hidden sm:block">
                                <div className="text-sm font-medium text-brand-text-heading">{user.name}</div>
                                <div className="text-xs text-brand-text-muted capitalize">
                                    {user.department ? `${user.department} Dept` : user.role}
                                </div>
                            </div>
                            <img
                                src={user.avatar}
                                alt={user.name}
                                className="w-8 h-8 rounded-full border-2 border-white shadow-sm object-cover"
                            />
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 scroll-smooth">
                    {children}
                </main>
            </div>
        </div>
    );
}

function NavItem({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
    return (
        <a href="#" className={cn(
            "flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
            active
                ? "bg-brand-primary/5 text-brand-primary"
                : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
        )}>
            {icon}
            <span>{label}</span>
            {active && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-brand-primary" />}
        </a>
    );
}
