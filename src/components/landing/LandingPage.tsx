import { useState, useEffect } from 'react';
import { ArrowRight, User, Briefcase, ShieldCheck, Activity, Globe, Server, Github, Twitter, Linkedin } from 'lucide-react';
import type { UserRole } from '../../types';

interface LandingPageProps {
    onLogin: (role: UserRole) => void;
}

export function LandingPage({ onLogin }: LandingPageProps) {
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => setIsScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const scrollToLogin = () => {
        document.getElementById('login-section')?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <div className="relative min-h-screen w-full font-sans text-white overflow-x-hidden">

            {/* Dynamic Background */}
            <div
                className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat transform scale-105 animate-[pulse_15s_ease-in-out_infinite]"
                style={{
                    backgroundImage: 'url("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80")',
                }}
            />

            {/* Gradient Overlay */}
            <div className="fixed inset-0 z-10 bg-gradient-to-b from-brand-primary/40 via-brand-primary/70 to-brand-primary/95 backdrop-blur-[2px]" />

            {/* Navbar */}
            <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-brand-primary/90 backdrop-blur-md py-4 shadow-lg' : 'bg-transparent py-6'}`}>
                <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-white to-brand-secondary flex items-center justify-center text-brand-primary font-bold text-xl shadow-lg">Z</div>
                        <span className="text-2xl font-bold tracking-tight">ZEdny</span>
                    </div>

                    <div className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-200">
                        <a href="#" className="hover:text-brand-secondary transition-colors">Services</a>
                        <a href="#" className="hover:text-brand-secondary transition-colors">Solutions</a>
                        <a href="#" className="hover:text-brand-secondary transition-colors">About</a>
                        <a href="#" className="hover:text-brand-secondary transition-colors">Contact</a>
                    </div>

                    <button
                        onClick={scrollToLogin}
                        className="px-6 py-2.5 rounded-full bg-white text-brand-primary font-semibold text-sm hover:bg-brand-secondary hover:text-white transition-all shadow-lg hover:shadow-brand-secondary/25"
                    >
                        Sign In
                    </button>
                </div>
            </nav>

            {/* Main Content */}
            <div className="relative z-20 pt-32 pb-20 px-4">

                {/* Hero Section */}
                <div className="min-h-[80vh] flex flex-col items-center justify-center text-center max-w-5xl mx-auto mb-20">
                    <div className="mb-8 animate-in fade-in slide-in-from-top-10 duration-1000">
                        <span className="px-4 py-2 rounded-full bg-brand-secondary/10 border border-brand-secondary/20 text-brand-secondary text-sm font-medium backdrop-blur-sm mb-6 inline-block">
                            ✨ Revolutionizing Enterprise Software
                        </span>
                        <h1 className="text-6xl md:text-8xl font-bold mb-8 leading-tight drop-shadow-2xl">
                            Building the <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-secondary to-blue-400">Future of AI</span>
                        </h1>
                        <p className="text-xl text-slate-200 max-w-2xl mx-auto font-light leading-relaxed mb-10 drop-shadow-md">
                            ZEdny connects visionary businesses with powerful AI solutions. Experience the next generation of software development and team collaboration.
                        </p>

                        <div className="flex items-center justify-center space-x-4">
                            <button onClick={scrollToLogin} className="px-8 py-4 rounded-full bg-brand-secondary text-brand-primary font-bold text-lg hover:bg-white transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1">
                                Get Started
                            </button>
                            <button className="px-8 py-4 rounded-full bg-white/10 border border-white/20 text-white font-medium text-lg hover:bg-white/20 transition-all backdrop-blur-md">
                                Learn More
                            </button>
                        </div>
                    </div>

                    {/* Stats Strip */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-16 pt-12 border-t border-white/10 w-full animate-in fade-in slide-in-from-bottom-10 duration-1000 delay-300">
                        <Stat label="Active Users" value="10k+" />
                        <Stat label="AI Models" value="50+" />
                        <Stat label="Enterprise Partners" value="120" />
                        <Stat label="Uptime" value="99.9%" />
                    </div>
                </div>

                {/* Login Section */}
                <div id="login-section" className="scroll-mt-32 max-w-6xl mx-auto mb-32">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">Choose Your Portal</h2>
                        <p className="text-slate-400">Secure access for clients, employees, and management</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <RoleCard
                            role="client"
                            title="Client Portal"
                            desc="Manage your projects and chat with our AI assistant"
                            icon={<User size={32} />}
                            onClick={() => onLogin('client')}
                            delay={0}
                        />
                        <RoleCard
                            role="employee"
                            title="Employee Workspace"
                            desc="Access internal tools, tasks, and reports"
                            icon={<Briefcase size={32} />}
                            onClick={() => onLogin('employee')}
                            delay={100}
                        />
                        <RoleCard
                            role="admin"
                            title="Admin Console"
                            desc="System overview and performance analytics"
                            icon={<ShieldCheck size={32} />}
                            onClick={() => onLogin('admin')}
                            delay={200}
                        />
                    </div>
                </div>

                {/* Footer */}
                <footer className="border-t border-white/10 pt-16 pb-8">
                    <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                        <div className="space-y-4">
                            <div className="flex items-center space-x-2 mb-4">
                                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-white to-brand-secondary flex items-center justify-center text-brand-primary font-bold">Z</div>
                                <span className="text-xl font-bold">ZEdny</span>
                            </div>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                Empowering businesses with intelligent software solutions. Innovating for a smarter tomorrow.
                            </p>
                            <div className="flex space-x-4">
                                <SocialIcon icon={<Twitter size={18} />} />
                                <SocialIcon icon={<Linkedin size={18} />} />
                                <SocialIcon icon={<Github size={18} />} />
                            </div>
                        </div>

                        <div>
                            <h4 className="font-bold mb-6">Solutions</h4>
                            <ul className="space-y-3 text-sm text-slate-400">
                                <FooterLink>AI Integration</FooterLink>
                                <FooterLink>Web Development</FooterLink>
                                <FooterLink>Cloud Infrastructure</FooterLink>
                                <FooterLink>Data Analytics</FooterLink>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold mb-6">Company</h4>
                            <ul className="space-y-3 text-sm text-slate-400">
                                <FooterLink>About Us</FooterLink>
                                <FooterLink>Careers</FooterLink>
                                <FooterLink>Blog</FooterLink>
                                <FooterLink>Contact</FooterLink>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold mb-6">Legal</h4>
                            <ul className="space-y-3 text-sm text-slate-400">
                                <FooterLink>Privacy Policy</FooterLink>
                                <FooterLink>Terms of Service</FooterLink>
                                <FooterLink>Security</FooterLink>
                            </ul>
                        </div>
                    </div>

                    <div className="text-center text-slate-500 text-xs pt-8 border-t border-white/5">
                        © 2025 ZEdny Systems Inc. All rights reserved.
                    </div>
                </footer>

                {/* Live Activity Widget */}
                <LiveActivityWidget />
            </div>
        </div>
    );
}

function Stat({ label, value }: { label: string, value: string }) {
    return (
        <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">{value}</div>
            <div className="text-xs text-brand-secondary uppercase tracking-wider">{label}</div>
        </div>
    );
}

function FooterLink({ children }: { children: React.ReactNode }) {
    return (
        <li><a href="#" className="hover:text-brand-secondary transition-colors">{children}</a></li>
    );
}

function SocialIcon({ icon }: { icon: React.ReactNode }) {
    return (
        <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-brand-secondary hover:text-white transition-all">
            {icon}
        </a>
    );
}

function RoleCard({ role, title, desc, icon, onClick, delay }: { role: string, title: string, desc: string, icon: React.ReactNode, onClick: () => void, delay: number }) {
    const colors = {
        client: "group-hover:border-brand-secondary group-hover:shadow-[0_0_50px_rgba(79,209,197,0.2)]",
        employee: "group-hover:border-brand-role-web group-hover:shadow-[0_0_50px_rgba(59,130,246,0.2)]",
        admin: "group-hover:border-brand-role-ai group-hover:shadow-[0_0_50px_rgba(139,92,246,0.2)]",
    };

    return (
        <button
            onClick={onClick}
            className={`group relative bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-3xl text-left transition-all duration-300 hover:-translate-y-2 hover:bg-white/10 ${colors[role as keyof typeof colors]}`}
            style={{ animationDelay: `${delay}ms` }}
        >
            <div className="mb-6 p-4 rounded-2xl bg-gradient-to-br from-white/10 to-transparent w-fit group-hover:scale-110 transition-transform duration-300 text-white group-hover:text-brand-secondary ring-1 ring-white/10">
                {icon}
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">{title}</h3>
            <p className="text-slate-400 text-sm mb-8 leading-relaxed">{desc}</p>

            <div className="flex items-center text-brand-secondary text-sm font-bold opacity-0 group-hover:opacity-100 transition-opacity transform translate-x-[-10px] group-hover:translate-x-0 duration-300">
                <span>Access Portal</span>
                <ArrowRight size={16} className="ml-2" />
            </div>
        </button>
    );
}

function LiveActivityWidget() {
    const [index, setIndex] = useState(0);

    const activities = [
        { icon: <Activity size={16} />, text: "AI Model v2.4 Training Complete", color: "text-green-400" },
        { icon: <Globe size={16} />, text: "New Client Onboarded: Dubai", color: "text-blue-400" },
        { icon: <Server size={16} />, text: "System Uptime: 99.99%", color: "text-brand-secondary" },
        { icon: <User size={16} />, text: "Active Agents: 124", color: "text-purple-400" },
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setIndex((prev) => (prev + 1) % activities.length);
        }, 4000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="hidden lg:flex fixed bottom-8 right-8 z-50 animate-in fade-in slide-in-from-right-10 duration-1000 delay-1000">
            <div className="bg-brand-primary/90 backdrop-blur-xl border border-white/10 rounded-full py-3 px-5 shadow-2xl flex items-center space-x-3 ring-1 ring-white/20">
                <div className="relative">
                    <div className="w-2 h-2 rounded-full bg-green-500" />
                    <div className="absolute inset-0 w-2 h-2 rounded-full bg-green-500 animate-ping" />
                </div>

                <div className="overflow-hidden h-6 w-64 relative">
                    {activities.map((item, i) => (
                        <div
                            key={i}
                            className={`absolute inset-0 flex items-center space-x-2 transition-all duration-500 transform ${i === index ? 'translate-y-0 opacity-100' :
                                i < index ? '-translate-y-full opacity-0' : 'translate-y-full opacity-0'
                                }`}
                        >
                            <span className={`${item.color}`}>{item.icon}</span>
                            <span className="text-xs font-medium text-slate-200">{item.text}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
