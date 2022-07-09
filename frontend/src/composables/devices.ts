import LedDevice from "@/components/devices/LedDevice.vue";

interface DeviceList {
  [key: string]: unknown;
}

/**
 * Returns a list of available devices.
 */
export function useDevice(deviceType: string): unknown {
  const devices: DeviceList = {
    LedDevice: LedDevice
  };
  return devices[deviceType];
}
