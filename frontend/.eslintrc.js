module.exports = {
  root: true,
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/eslint-config-typescript/recommended"
  ],
  env: {
    "vue/setup-compiler-macros": true,
    node: true
  },
  overrides: [],
  rules: {
    "vue/script-setup-uses-vars": "error"
  }
};
