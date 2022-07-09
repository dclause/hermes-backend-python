import { defineStore } from "pinia";

export type DeviceConfigurationProperties = {
  name: string;
  id: number;
  board: number;
  state: unknown;

  [x: string]: unknown;
}

export const useDeviceStore = defineStore({
  id: "devices",
  state: () => ({
    devices: {} as Record<number, DeviceConfigurationProperties>
  }),
  getters: {
    getDevice: (state) => {
      return (id: number) => state.devices[id] as DeviceConfigurationProperties;
    }
  },
  actions: {
    patch(device_id: number, partial: Record<string, unknown>) {
      this.devices[device_id].name += "test";
    }
  }
});
