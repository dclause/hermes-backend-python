import ArduinoBoard from "@/components/boards/ArduinoBoard.vue";

interface BoardList {
  [key: string]: unknown;
}

/**
 * Returns a list of available boards.
 */
export function useBoard(boardType: string): unknown {
  const boards: BoardList = {
    ArduinoBoard: ArduinoBoard
  };
  return boards[boardType];
}
