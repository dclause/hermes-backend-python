/**
 * Instantiates Vuetify via createVuetify() helper to be used in main.ts.
 *
 * Documentation: https://next.vuetifyjs.com/en/
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "@/styles/_variables.scss";

// Vuetify
import type { ThemeDefinition } from "vuetify";
import { createVuetify } from "vuetify";

// Light custom theme (based on vuetify 2 default color scheme).
const light: ThemeDefinition = {
  dark: false,
  colors: {
    background: "#FFFFFF",
    surface: "#FFFFFF",
    primary: "#1976D2",
    secondary: "#424242",
    accent: "#82B1FF",
    error: "#FF5252",
    info: "#2196F3",
    success: "#4CAF50",
    warning: "#FFC107",
  },
};

export default createVuetify({
  theme: {
    defaultTheme: "light",
    themes: {
      light,
    },
  },
});
