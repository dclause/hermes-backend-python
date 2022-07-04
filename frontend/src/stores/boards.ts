import { defineStore } from "pinia";

export const useBoardStore = defineStore({
  id: "boards",
  state: (): Record<string, any> => ({
    boards: {},
  }),
  getters: {
    getBoard: (state) => {
      return (id: string) => state.boards[id];
    },
  },
  actions: {},
});
