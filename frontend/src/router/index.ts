import { createRouter, createWebHistory } from "vue-router";
import BoardPage from "../pages/BoardPage.vue";
import BoardListPage from "../pages/BoardListPage.vue";
import DeviceListPage from "../pages/DeviceListPage.vue";
import HomePage from "../pages/HomePage.vue";

const router = createRouter({
  history: createWebHistory(),
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
      path: "/board/:boardId",
      name: "board",
      component: BoardPage
    },
    {
      path: "/devices",
      name: "devices",
      component: DeviceListPage
    }
  ]
});

export default router;
