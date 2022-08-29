import BoardListPage from "../pages/BoardListPage.vue";
import BoardPage from "../pages/BoardPage.vue";

export default [
  {
    path: "/board/all",
    name: "boards",
    component: BoardListPage
  },
  {
    path: "/board/:boardId(\\d+)",
    name: "board",
    component: BoardPage
  }
];
