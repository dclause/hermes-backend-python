import ArduinoBoard from "@/components/boards/ArduinoBoard.vue";
import type { Component } from "vue";

interface BoardList {
  [key: string]: Component;
}

/**
 * Returns a list of available boards.
 */
export function useBoard(boardType: string): Component {
  const boards: BoardList = {
    ArduinoBoard: ArduinoBoard,
  };
  return boards[boardType];
}
