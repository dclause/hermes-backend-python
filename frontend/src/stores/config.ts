import type { PiniaCustomStateProperties } from "pinia";
import { defineStore } from "pinia";

export declare interface ConfigurationProperties
  extends PiniaCustomStateProperties {
  connected: boolean;
  server?: ServerConfigurationProperties;
  web?: ServerConfigurationProperties;
}

export declare interface ServerConfigurationProperties extends Object {
  host?: string;
  port?: number;
  debug?: boolean;
  enabled?: boolean;
}

export const useConfigStore = defineStore({
  id: "config",
  state: (): ConfigurationProperties => ({
    connected: false
  }),
  getters: {},
  actions: {}
});
