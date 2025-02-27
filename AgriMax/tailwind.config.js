/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './AgriMaxApp/templates/*.html',
    './AgriMaxApp/static/js/*.js'

  ],
  theme: {
    extend: {
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
  variants: {
    extend: {
      //backgroundImage: ['dark'],
    },
  },
  arbitraryValues: {
    width: true,
    height: true,
  },
};
