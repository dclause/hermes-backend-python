import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueI18n from "@intlify/vite-plugin-vue-i18n";

// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
import vuetify from "vite-plugin-vuetify";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 4000,
    host: true,
    hmr: {
      port: 4010,
    },
    watch: {
      usePolling: true,
    },
  },
  plugins: [
    vue(),
    vueI18n({
      include: resolve(__dirname, "./locales/**"),
      runtimeOnly: false,
    }),
    vuetify({ autoImport: true, styles: "expose" }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
