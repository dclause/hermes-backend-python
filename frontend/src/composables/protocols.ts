import SerialProtocol from "@/components/protocols/SerialProtocol.vue";
import CustomProtocol from "@/components/protocols/CustomProtocol.vue";

export type ProtocolConfigurationProperties = {
  id: number,
  name?: string,
  controller: string,
  [x: string]: unknown;
}

/**
 * Returns a list of available protocols.
 * Defaults to CustomProtocol if not existing.
 */
export function useProtocol(protocolType: string): unknown {
  const commands: Record<string, unknown> = {
    SerialProtocol: SerialProtocol
  };
  return commands[protocolType] ?? CustomProtocol;
}

