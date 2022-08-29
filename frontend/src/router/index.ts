import { createRouter, createWebHistory } from "vue-router";
import DeviceListPage from "@/pages/DeviceListPage.vue";
import NotFoundPage from "@/pages/NotFoundPage.vue";
import HomePage from "@/pages/HomePage.vue";
import boardPages from "./boards";

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
    ...boardPages,
    {
      path: "/devices",
      name: "devices",
      component: DeviceListPage
    },
    {
      path: "/:catchAll(.*)*",
      name: "404",
      component: () => NotFoundPage,
      meta: {
        layout: "SimpleLayout"
      }
    }
  ]
});

export default router;
