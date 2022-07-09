import { createRouter, createWebHistory } from "vue-router";
import BoardListPage from "../pages/BoardListPage.vue";
import DeviceListPage from "../pages/DeviceListPage.vue";
import HomePage from "../pages/HomePage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      path: "/boards",
      name: "boards",
      component: BoardListPage
    },
    {
      path: "/devices",
      name: "devices",
      component: DeviceListPage
    }
  ]
});

export default router;
