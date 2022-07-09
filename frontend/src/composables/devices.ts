import LedDevice from "@/components/devices/LedDevice.vue";
import type { Component } from "vue";

interface DeviceList {
  [key: string]: Component;
}

/**
 * Returns a list of available devices.
 */
export function useDevice(deviceType: string): Component {
  const devices: DeviceList = {
    LedDevice: LedDevice
  };
  return devices[deviceType];
}
