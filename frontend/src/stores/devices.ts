import { defineStore } from "pinia";

export const useDeviceStore = defineStore({
  id: "devices",
  state: (): Record<string, any> => ({
    devices: {},
  }),
  getters: {
    getDevice: (state) => {
      return (id: string) => state.devices[id];
    },
  },
  actions: {},
});
