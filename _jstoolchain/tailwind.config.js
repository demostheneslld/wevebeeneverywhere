const colors = require('tailwindcss/colors');

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      gray: colors.coolGray,
      primary: colors.coolGray,
      accent: colors.blue,
      black: colors.black,
      white: colors.white,
      bad: colors.red,
      good: colors.green,
      warn: colors.amber,
    },
    extend: {},
  },
  variants: {
    extend: {
      ringWidth: ['focus-visible'],
      ringColor: ['focus-visible'],
    },
  },
  plugins: [],
}
