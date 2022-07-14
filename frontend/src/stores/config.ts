import { defineStore } from "pinia";

export declare interface ConfigurationProperties {
  connected: boolean;
  server?: ServerConfigurationProperties;
  web?: ServerConfigurationProperties;
}

export declare interface ServerConfigurationProperties {
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
