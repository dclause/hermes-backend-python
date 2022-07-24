#ifndef ARDUINO_COMMAND_FACTORY_H
#define ARDUINO_COMMAND_FACTORY_H

#include "../helper/map.h"
#include "CommandCode.h"
#include "AbstractCommand.h"

// Callback for instantiating "on the fly" a command.
using CommandInstance = AbstractCommand *(*)();

/**
 * Command Factory: registers command and instantiates it as necessary from a given command code.
 *
 * @note
 * Command codes are mapped to actual commands via the CommandFactory by registering the command class to the factory
 * keyed by the appropriate command code. This is done via the conjunction usage of the macros `COMMAND_DECLARATION`
 * and `REGISTER_COMMAND(N, T)`.
 */
class CommandFactory {
    private:
        CommandFactory() = default;

        KeyValueMap<CommandCode, CommandInstance> registeredCommands_;

    public:
        CommandFactory(const CommandFactory &) = delete;

        CommandFactory &operator=(const CommandFactory &) = delete;

        static CommandFactory &getInstance() {
            static CommandFactory instance;
            return instance;
        }

        /**
         * Let a CommandCode be associated to an instantiable callback.
         * Stores this association in the internal map.
         *
         * @param code (CommandCode)
         * @param callback (CommandInstance) @see `using` statement at the start of file.
         * @return bool: If the command is properly registered.
         */
        bool registerCommand(CommandCode code, CommandInstance callback) {
            return this->registeredCommands_.add(code, callback);
        }

        /**
         * Instantiates an AbstractCommand of the proper type given a CommandCode.
         *
         * @note
         * A proper command is always instantiated. If the CommandCode is unknown or if something goes wrong, the
         * VOID command is returned.
         * @see VoidCommand
         *
         * @param code (CommandCode)
         * @return AbstractCommand: The instantiated command class.
         */
        AbstractCommand *createCommand(CommandCode code) {
            CommandInstance command = this->registeredCommands_.getValue(code);
            if (command == NULL) { return NULL; }
            return command();
        }

        /**
         * Stringifies the data for debug purpose.
         *
         * @return String
         */
        operator String() {
            String log =
                    (String) F("Command Factory ") + (String) this->registeredCommands_.count() + (String) F(":\n");
            for (uint8_t i = 0; i < this->registeredCommands_.count(); i++) {
                AbstractCommand *command = this->registeredCommands_.get(i)->value();
                log += (String) F("# - ") + (String) *command + F("\n");
            }
            return log;
        }
};

#define COMMAND_DECLARATION protected: \
    static AbstractCommand* getInstance(); \
    static bool isRegistered;
#define GET_COMMAND_INSTANCE(T) AbstractCommand* T::getInstance() { return new T(); }
#define REGISTER_COMMAND(N, T) bool T::isRegistered = CommandFactory::getInstance().registerCommand(N, &T::getInstance);GET_COMMAND_INSTANCE(T);

#endif // ARDUINO_COMMAND_FACTORY_H
