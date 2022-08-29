import { createRouter, createWebHistory } from "vue-router";
import boardPages from "./boards";
import DeviceListPage from "@/pages/DeviceListPage.vue";
import HomePage from "@/pages/HomePage.vue";
import NotFoundPage from "@/pages/NotFoundPage.vue";
import SettingsPage from "@/pages/SettingsPage.vue";

const router = createRouter({
  history: createWebHistory(),
  strict: true,
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../pages/AboutPage.vue")
    },
    {
      path: "/settings",
      name: "settings",
      component: () => SettingsPage,
      meta: {
        layout: "SimpleLayout"
      }
    },
    ...boardPages,
    {
      path: "/devices",
      name: "devices",
      component: DeviceListPage
    },
    {
      path: "/:catchAll(.*)*",
      name: "404",
      component: NotFoundPage,
      meta: {
        layout: "SimpleLayout"
      }
    }
  ]
});

export default router;
