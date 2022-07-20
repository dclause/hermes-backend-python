import { defineStore } from "pinia";

export declare interface ProfileProperties {
  name: string;
  description: string;
}

export const useProfileStore = defineStore({
  id: "profile",
  state: (): ProfileProperties => ({
    name: "a Robot Management System",
    description: "No profile loaded"
  }),
  getters: {},
  actions: {}
});
