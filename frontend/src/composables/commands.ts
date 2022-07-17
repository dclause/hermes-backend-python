import BooleanAction from "@/components/commands/BooleanAction.vue";
import UnknownCommand from "@/components/commands/UnknownCommand.vue";

export type CommandConfigurationProperties = {
  id: number,
  name?: string,
  type: string,
  default: unknown
  state: unknown
  [x: string]: unknown;
}

/**
 * Returns a list of available boards.
 * @todo can we avoid this ?
 */
export function useCommand(commandType: string): unknown {
  const commands: Record<string, unknown> = {
    BOOLEAN_ACTION: BooleanAction,
    ON_OFF: BooleanAction
  };
  return commands[commandType] ?? UnknownCommand;
}

