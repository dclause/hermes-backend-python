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
 * Returns the command component to use among available list.
 * Defaults to UnknownCommand if not given.
 *
 * @note: this is done to avoid lazy-loading components.
 * It may seem opposite to usual performance recommendations, but we want here
 * to avoid any extra server work or network load once the UI is started, hence
 * we are okay with a longer initial load time.
 */
export function useCommand(commandType: string): unknown {
  const commands: Record<string, unknown> = {
    BooleanAction: BooleanAction,
    ServoAction: ServoAction
  };
  return commands[commandType] ?? UnknownCommand;
}

/**
 * Builds the tooltip info for a command.
 * @param command
 * @param props
 */
export function useCommandInfoComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.info !== undefined) {
      return props.info;
    }
    const board = props.board as BoardConfigurationProperties;
    return `Board "${board.name}" (PIN ${command.pin}): ${command.state}`;
  });
}

/**
 * Builds the label for a command.
 * @param command
 * @param props
 */
export function useCommandLabelComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.label !== undefined) {
      return props.label;
    }
    return `Command "${command.name}" :`;
  });
}

/**
 * Builds the feedback info for a command.
 * @param command
 * @param props
 */
export function useCommandFeedbackComputed(command: CommandConfigurationProperties, props: Record<string, unknown>): unknown {
  return computed(() => {
    if (props.feedback !== undefined) {
      return props.feedback;
    }
    return `PIN ${command.pin}: ${command.state}`;
  });
}

/**
 * Default common props for a command.
 */
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