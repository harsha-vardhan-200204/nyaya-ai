/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f4f8',
          100: '#dbe3ed',
          200: '#bcd0e6',
          300: '#91b2d7',
          400: '#608fc4',
          500: '#102c57', // Deep Navy Primary
          600: '#0d2346',
          700: '#0a1a35',
          800: '#071224',
          900: '#030812',
        },
        gold: {
          50: '#fbf8eb',
          100: '#f6eed0',
          200: '#eedea0',
          300: '#e3c667',
          400: '#d7aa35',
          500: '#b48c28', // Gold Accent
          600: '#9a7520',
          700: '#805f1a',
          800: '#664a14',
          900: '#4d360f',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
