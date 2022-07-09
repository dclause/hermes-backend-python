import { defineStore } from "pinia";

export declare interface BoardConfigurationProperties extends Object {
  name: string;
  id: number;
  model: string;

  [x: string]: unknown;
}

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
