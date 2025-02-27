/** @type {import('tailwindcss').Config} */
//darkMode: 'selector', '[data-mode="dark"]'],
module.exports = {
    content: ['./templates/login.html',
        './static/*.js',
    ],
    plugin: [
        require('autoprefixer'),
    ],
    variants: {
        darkMode: ['class'],
        hover: ['class'],
        focus: ['class'],
    },
    theme: {
        colors: {
            primary: '#3498db',
            secondary: '#f1c40f',
            accent: '#e74c3c',
        },
        spacing: {
            sm: '8px',
            md: '16px',
            lg: '24px',
            xl: '32px',
        },
        typography: {
            fontFamily: {
                sans: ['Open Sans', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
            },
            fontSize: {
                sm: '14px',
                md: '16px',
                lg: '18px',
                xl: '20px',
            },
        },
    },
    plugins: [],
}
