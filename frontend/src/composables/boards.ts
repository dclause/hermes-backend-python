import ArduinoBoard from "@/components/boards/ArduinoBoard.vue";
import CustomBoard from "@/components/boards/CustomBoard.vue";
import type { CommandConfigurationProperties } from "@/composables/commands";

export declare type BoardConfigurationProperties = {
  id: number,
  name?: string,
  model: string,
  actions: CommandConfigurationProperties[],
  inputs: CommandConfigurationProperties[],
  [x: string]: unknown,
}

/**
 * Returns the board component to use among available list.
 * Defaults to CustomBoard if not given.
 *
 * @note: this is done to avoid lazy-loading components.
 * It may seem opposite to usual performance recommendations, but we want here
 * to avoid any extra server work or network load once the UI is started, hence
 * we are okay with a longer initial load time.
 */
export function useBoard(boardType: string): unknown {
  const boards: Record<string, unknown> = {
    ArduinoBoard: ArduinoBoard
  };
  return boards[boardType] ?? CustomBoard;
}

export function useBoardController(boardType: string): string {
  switch (boardType) {
    case "ArduinoBoard":
      return "Arduino";
    default:
      return boardType;
  }
}