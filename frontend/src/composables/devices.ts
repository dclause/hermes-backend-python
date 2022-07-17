import LedDevice from "@/components/devices/LedDevice.vue";
import CustomDevice from "@/components/devices/CustomDevice.vue";
import { CommandConfigurationProperties } from "@/composables/commands";

export type DeviceConfigurationProperties = {
  id: number;
  name?: string;
  board: number;
  actions: [CommandConfigurationProperties]
  inputs: [CommandConfigurationProperties]
  [x: string]: unknown;
}


/**
 * Returns a list of available devices.
 */
export function useDevice(deviceType: string): unknown {
  const devices: Record<string, unknown> = {
    LedDevice: LedDevice,
    CustomDevice: CustomDevice
  };
  return devices[deviceType] ?? CustomDevice;
}
