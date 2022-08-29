import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import pinia from "./plugins/pinia";
import { socketIO } from "./plugins/socketIO";
import ConnectedLayout from "@/layouts/ConnectedLayout.vue";
import SimpleLayout from "@/layouts/SimpleLayout.vue";


const app = createApp(App).use(router).use(vuetify).use(socketIO).use(pinia);
app.component("ConnectedLayout", ConnectedLayout);
app.component("SimpleLayout", SimpleLayout);
app.mount("#app");
