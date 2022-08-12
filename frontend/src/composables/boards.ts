import CustomBoard from "@/components/boards/CustomBoard.vue";

export declare interface BoardConfigurationProperties {
  id: number,
  name?: string,
  model: string,

  [x: string]: unknown,
}

/**
 * Returns a list of available boards.
 * Defaults to UnknownBoard if not existing.
 */
export function useBoard(boardType: string): unknown {
  const boards: Record<string, unknown> = {
    // ArduinoBoard: ArduinoBoard
  };
  return boards[boardType] ?? CustomBoard;
}
