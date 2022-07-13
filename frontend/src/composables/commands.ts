/**
 * Returns a list of available commands.
 *
 * @todo export this enum to a single 'knowledge dictionary' file and create a code generator to make it.
 * The purpose would be to not repeat the enum thought all languages and parts of the project.
 * @see frontend/composables/commands.ts
 * @see backend/hermes/core/commands/__init__/py
 * @see arduino/Commands/CommandCode.h
 */
export enum useCommand {
  DIGITAL_WRITE = 42,
  BLINK = 98,
  ON_OFF = 99
}
