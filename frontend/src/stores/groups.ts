import { defineStore } from "pinia";
import type { GroupConfigurationProperties } from "@/composables/groups";

export const useGroupStore = defineStore({
  id: "groups",
  state: () => ({
    groups: [] as GroupConfigurationProperties[]
  }),
  getters: {
    getGroup: (state) => {
      return (id: number) => state.groups.find(group => group.id === id);
    }
  },
  actions: {}
});
