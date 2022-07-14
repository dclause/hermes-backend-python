import BooleanCommand from "@/components/commands/BooleanCommand.vue";
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
 * Returns a list of available commands.
 *
 * @todo export this enum to a single 'knowledge dictionary' file and create a code generator to make it.
 * The purpose would be to not repeat the enum thought all languages and parts of the project.
 * @see frontend/composables/commands.ts
 * @see backend/hermes/core/commands/__init__/py
 * @see arduino/Commands/CommandCode.h
 */
export enum CommandType {
  DIGITAL_WRITE = 42,
}

/**
 * Returns a list of available boards.
 */
export function useCommand(commandType: string): unknown {
  const commands: Record<string, unknown> = {
    BOOLEAN: BooleanCommand
  };
  return commands[commandType] ?? UnknownCommand;
}

