import BooleanAction from "@/components/commands/BooleanAction.vue";
import ServoAction from "@/components/commands/ServoAction.vue";
import UnknownCommand from "@/components/commands/UnknownCommand.vue";
import { computed } from "vue";
import { BoardConfigurationProperties } from "@/composables/boards";

export type CommandConfigurationProperties = {
  id: number,
  name?: string,
  controller: string,
  default: unknown,
  state: unknown,
  [x: string]: unknown,
}

/**
 * Returns a list of available commands.
 * Defaults to UnknownCommand if not existing.
 */
export function useCommand(commandType: string): unknown {
  const commands: Record<string, unknown> = {
    BooleanAction: BooleanAction,
    ServoAction: ServoAction
  };
  return commands[commandType] ?? UnknownCommand;
}

export function useCommandInfoComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.info !== undefined) {
      return props.info;
    }
    const board = props.board as BoardConfigurationProperties;
    return `Board "${board.name}" (PIN ${command.pin}): ${command.state}`;
  });
}

export function useCommandLabelComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.label !== undefined) {
      return props.label;
    }
    return `Command "${command.name}" :`;
  });
}

export function useCommandFeedbackComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.feedback !== undefined) {
      return props.feedback;
    }
    return `PIN ${command.pin}: ${command.state}`;
  });
}

export function useCommandProps() {
  return defineProps({
    modelValue: {
      type: Object,
      required: true
    },
    board: {
      type: Object,
      required: true
    },
    label: {
      type: String,
      default: undefined
    },
    info: {
      type: String,
      default: undefined
    },
    feedback: {
      type: String,
      default: undefined
    }
  });
}