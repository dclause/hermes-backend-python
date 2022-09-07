import { defineStore } from "pinia";
import type { DeviceConfigurationProperties } from "@/composables/devices";

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
      const partial_tmp = { name: this.devices[device_id].name + "test" };
      this.devices[device_id] = { ...this.devices[device_id], ...partial_tmp };
    }
  }
});
