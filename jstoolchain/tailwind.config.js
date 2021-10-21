const colors = require('tailwindcss/colors');

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      gray: colors.coolGray,
      primary: colors.coolGray,
      accent: colors.blue,
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
