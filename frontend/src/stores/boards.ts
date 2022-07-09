import { defineStore } from "pinia";

export declare interface BoardConfigurationProperties extends Object {
  name: string;
  id: string;
  model: string;

  [x: string]: unknown;
}

export const useBoardStore = defineStore({
  id: "boards",
  state: () => ({
    boards: {} as Record<string, BoardConfigurationProperties>
  }),
  getters: {
    getBoard: (state) => {
      return (id: string) => state.boards[id] as BoardConfigurationProperties;
    }
  },
  actions: {}
});
