import SerialProtocol from "@/components/protocols/SerialProtocol.vue";
import CustomProtocol from "@/components/protocols/CustomProtocol.vue";

export type ProtocolConfigurationProperties = {
  id: number,
  name?: string,
  controller: string,
  [x: string]: unknown;
}

/**
 * Returns the protocol component to use among available list.
 * Defaults to CustomProtocol if not given.
 *
 * @note: this is done to avoid lazy-loading components.
 * It may seem opposite to usual performance recommendations, but we want here
 * to avoid any extra server work or network load once the UI is started, hence
 * we are okay with a longer initial load time.
 */
export function useProtocol(protocolType: string): unknown {
  const commands: Record<string, unknown> = {
    SerialProtocol: SerialProtocol
  };
  return commands[protocolType] ?? CustomProtocol;
}

