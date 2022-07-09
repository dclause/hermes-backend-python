/**
 * Instantiates socketIO to be used in main.ts.
 */

import { io } from "socket.io-client";
import type { App, Plugin } from "vue";
import { inject } from "vue";
import type { Socket } from "socket.io-client/build/esm/socket";

export const socketIO: Plugin = {
  install: (app: App) => {
    // Define the socket.
    // @todo find a way to make it sort of configurable ? (window.location.port)
    const socket = io(window.location.hostname + ":9999", {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 99999
    }) as Socket;
    // Globally accessible $socket (better)
    app.config.globalProperties.$socket = socket;
    // Globally provide/inject socket (@see useSocket()).
    app.provide("socket", socket);
  }
};

export function useSocket(): Socket {
  return inject("socket") as Socket;
}
