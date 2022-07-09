import { defineStore } from "pinia";

export declare interface DeviceConfigurationProperties extends Object {
  name: string;
  id: string;
  board: string;

  [x: string]: unknown;
}

export const useDeviceStore = defineStore({
  id: "devices",
  state: () => ({
    devices: {} as Record<string, DeviceConfigurationProperties>
  }),
  getters: {
    getDevice: (state) => {
      return (id: string) => state.devices[id] as DeviceConfigurationProperties;
    }
  },
  actions: {}
});
