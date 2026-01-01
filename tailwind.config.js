/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    primary: '#1E2A44',   // Deep Indigo / Blue
                    secondary: '#4FD1C5', // Soft Cyan
                    bg: '#F8FAFC',        // Background
                    card: '#FFFFFF',      // Card White
                    text: {
                        heading: '#0F172A',
                        body: '#475569',
                        muted: '#94A3B8'
                    }
                },
                role: {
                    client: '#4FD1C5',
                    web: '#3B82F6',
                    ai: '#8B5CF6',
                    content: '#F59E0B'
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
