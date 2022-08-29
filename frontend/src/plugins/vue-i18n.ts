/**
 * Instantiates vue-i18n via createI18n() helper to be used in main.ts and vuetitfy.ts plugin.
 *
 * Documentation: https://vue-i18n.intlify.dev/
 * Vuetify integration: https://next.vuetifyjs.com/en/features/internationalization/
 */
import { createI18n } from "vue-i18n";
import translationEN from "@/translations/en";
import translationFR from "@/translations/fr";

const messages = {
  en: translationEN,
  fr: translationFR
};

export default createI18n({
  legacy: false, // Vuetify does not support the legacy mode of vue-i18n
  locale: navigator.language.split("-")[0],
  fallbackLocale: "en",
  messages
});
