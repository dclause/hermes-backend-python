import { defineStore } from "pinia";
import { socket } from "@/plugins/socketIO";

export const useCommandStore = defineStore("commands", {
  state: () => ({}),
  getters: {},
  actions: {
    /**
     * Forward the command via the backend socketIO connexion to the robot.
     * @see backend/hermes/core/server.py
     */
    sendCommand(device_id: number, command_id: number, value: unknown) {
      socket.emit("action", device_id, command_id, value);
    }
  }
});
