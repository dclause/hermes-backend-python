/**
 * Instantiates socketIO to be used in main.ts.
 */

import { io } from "socket.io-client";
import type { App } from "vue";
import { inject } from "vue";
import type { Socket } from "socket.io-client/build/esm/socket";

export const socketIO = {
  install: (app: App) => {
    const socket = io(window.location.hostname + ":9999", {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 99999,
    }) as Socket;
    app.config.globalProperties.$socket = socket;
    app.provide("socket", socket);
  },
};

export function useSocket(): Socket {
  return inject("socket") as Socket;
}
