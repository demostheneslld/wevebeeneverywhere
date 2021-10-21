const colors = require('tailwindcss/colors');

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      gray: {
        ...colors.coolGray,
        50: '#F7F9FC',
      },
      primary: {
        ...colors.coolGray,
        50: '#F7F9FC',
      },
      accent: {
        50: '#f0faff',
        100: '#dbf3ff',
        200: '#ade4ff',
        300: '#7ad3ff',
        400: '#44BCFF',
        500: '#2685b5',
        600: '#186890',
        700: '#115374',
        800: '#0b3d56',
        900: '#02283b',
      },
      white: colors.white,
      bad: colors.red,
      good: colors.green,
      warn: colors.amber,
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
