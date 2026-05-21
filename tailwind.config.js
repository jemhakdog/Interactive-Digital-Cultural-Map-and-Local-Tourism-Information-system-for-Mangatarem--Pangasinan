/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html", "./static/js/**/*.js", "./static/css/**/*.css"],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                    950: '#082f49',
                },
                accent: '#D4AF37', // Antique Heritage Gold
                'sapphire-black': '#0f172a', // Deep sapphire/slate (slate-900)
                'premium-blue': '#38bdf8', // Premium Sky Blue (sky-400)
                'royal-blue': '#1d4ed8', // Professional Royal Blue (blue-700)
                'action-blue': '#006cfa',
                'hover-blue': '#3860be',
                'teal-active': '#1eaedb',
                'deep-teal': '#1c2d38',
                'teal-gray': '#3d4f58',
                'silver-teal': '#b8c4c2',
                'light-input': '#e8edeb',
            },
            fontFamily: {
                display: ['"MongoDB Value Serif"', '"Playfair Display"', 'serif'],
                body: ['"Euclid Circular A"', '"Plus Jakarta Sans"', 'sans-serif'],
                code: ['"Source Code Pro"', 'monospace'],
                serif: ['"Noto Serif TC"', 'serif'],
                sans: ['"Noto Sans TC"', 'sans-serif'],
            },
            boxShadow: {
                'forest': 'rgba(0, 30, 43, 0.12) 0px 26px 44px, rgba(0, 0, 0, 0.13) 0px 7px 13px',
                'standard': 'rgba(0, 0, 0, 0.15) 0px 3px 20px',
                'subtle': 'rgba(0, 0, 0, 0.1) 0px 2px 4px',
            },
            animation: {
                'aurora-slow': 'aurora 20s linear infinite',
                'aurora-fast': 'aurora 10s linear infinite',
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
            },
            keyframes: {
                aurora: {
                    '0%, 100%': { backgroundPosition: '0% 50%' },
                    '50%': { backgroundPosition: '100% 50%' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [],
}
