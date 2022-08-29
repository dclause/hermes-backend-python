/**
 * Instantiates Vuetify via createVuetify() helper to be used in main.ts.
 *
 * Documentation: https://next.vuetifyjs.com/en/
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "@/styles/_variables.scss";

import { createVuetify } from "vuetify";
import { createVueI18nAdapter } from "vuetify/locale/adapters/vue-i18n";
import { useI18n } from "vue-i18n";
import i18n from "./vue-i18n";

export default createVuetify({
  locale: createVueI18nAdapter({ i18n, useI18n }),
  theme: {
    // options: { customProperties: true },
    defaultTheme: "light",
    themes: {
      // Light custom theme (based on vuetify 2 default color scheme).
      light: {
        colors: {
          background: "#D7D7D7",
          surface: "#FFFFFF",
          primary: "#1976D2",
          secondary: "#424242",
          accent: "#82B1FF",
          error: "#FF5252",
          info: "#2196F3",
          success: "#4CAF50",
          warning: "#FFC107"
        }
      }
    }
  }
});
