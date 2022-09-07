import { createRouter, createWebHistory } from "vue-router";
import boardPages from "./boards";
import AboutPage from "@/pages/AboutPage.vue";
import GroupListPage from "@/pages/GroupListPage.vue";
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
      component: AboutPage
    },
    {
      path: "/settings",
      name: "settings",
      component: SettingsPage,
      meta: {
        layout: "SimpleLayout"
      }
    },
    ...boardPages,
    {
      path: "/groups",
      name: "groups",
      component: GroupListPage
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
