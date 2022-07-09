/**
 * Returns a list of available commands.
 *
 * @todo export this enum to a single 'knownledge dictionary' file and create a code generator to make it.
 * The purpose would be to not repeat the enum thought all languages and parts of the project.
 * @see frontend/composables/commands.ts
 * @see backend/hermes/core/commands/__init__/py
 * @see arduino/Commands/CommandCode.h
 */
export enum useCommand {
  ON_OFF = 98   // ascii: c
}
