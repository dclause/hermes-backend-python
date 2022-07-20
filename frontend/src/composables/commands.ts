import BooleanAction from "@/components/commands/BooleanAction.vue";
import UnknownCommand from "@/components/commands/UnknownCommand.vue";

export type CommandConfigurationProperties = {
  id: number,
  name?: string,
  controller: string,
  default: unknown
  state: unknown
  [x: string]: unknown;
}

/**
 * Returns a list of available commands.
 */
export function useCommand(commandType: string): unknown {
  const commands: Record<string, unknown> = {
    BooleanAction: BooleanAction
  };
  return commands[commandType] ?? UnknownCommand;
}

