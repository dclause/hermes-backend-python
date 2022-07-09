import { defineStore } from "pinia";

export const useLedStore = defineStore({
  id: "led",
  state: () => ({
    led: false
  }),
  getters: {},
  actions: {
    turnOn() {
      this.led = true;
    },
    turnOff() {
      this.led = false;
    }
  }
});
