/**
 * Instantiates socketIO to be used in main.ts.
 */

import { io } from "socket.io-client";
import type { App, Plugin } from "vue";
import { inject } from "vue";
import type { Socket } from "socket.io-client/build/esm/socket";

// @todo find a way to make it sort of configurable ? (window.location.port)
export const socket = io(window.location.hostname + ":9999", {
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: 99999
}) as Socket;

export const socketIO: Plugin = {
  install: (app: App) => {
    // Globally accessible $socket (better)
    app.config.globalProperties.$socket = socket;
    // Globally provide/inject socket (@see useSocket()).
    app.provide("socket", socket);
  }
};

export function useSocket(): Socket {
  return inject("socket") as Socket;
}
