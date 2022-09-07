import GenericDevice from "@/components/devices/GenericDevice.vue";
import LedDevice from "@/components/devices/LedDevice.vue";
import ServoDevice from "@/components/devices/ServoDevice.vue";
import type { CommandConfigurationProperties } from "@/composables/commands";

export type DeviceConfigurationProperties = {
  id: number;
  name?: string;
  board: number;
  actions: [CommandConfigurationProperties]
  inputs: [CommandConfigurationProperties]
  [x: string]: unknown;
}


/**
 * Returns the device component to use among available list.
 * Defaults to CustomDevice if not given.
 *
 * @note: this is done to avoid lazy-loading components.
 * It may seem opposite to usual performance recommendations, but we want here
 * to avoid any extra server work or network load once the UI is started, hence
 * we are okay with a longer initial load time.
 */
export function useDevice(deviceType: string): unknown {
  const devices: Record<string, unknown> = {
    LedDevice: LedDevice,
    ServoDevice: ServoDevice
  };
  return devices[deviceType] ?? GenericDevice;
}
