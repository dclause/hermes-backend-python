/**
 * Instantiates socketIO to be used in main.ts.
 */

import { io } from "socket.io-client";

export const useSocketIO = () => {
  const socket = io("http://localhost:4444");
  return {
    socket,
  };
};
