import { defineStore } from "pinia";
import type { BoardConfigurationProperties } from "@/composables/boards";

export const useBoardStore = defineStore({
  id: "boards",
  state: () => ({
    boards: {} as Record<number, BoardConfigurationProperties>
  }),
  getters: {
    getBoard: (state) => {
      return (id: number) => state.boards[id] as BoardConfigurationProperties;
    }
  },
  actions: {}
});
