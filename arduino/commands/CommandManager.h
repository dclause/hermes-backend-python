#ifndef ARDUINO_COMMAND_MANAGER_H
#define ARDUINO_COMMAND_MANAGER_H

#include <Arduino.h>
#include "../helper/map.h"
#include "AbstractCommand.h"

/**
 * Runnable manager: keeps track of all runnable commands.
 * @see AbstractCommand.h
 */
class RunnableManager {
    private:
        RunnableManager() = default;

        KeyValueMap<uint8_t, AbstractCommand *> runnables_;

    public:
        RunnableManager(const RunnableManager &) = delete;

        RunnableManager &operator=(const RunnableManager &) = delete;

        static RunnableManager &getInstance() {
            static RunnableManager instance;
            return instance;
        }

        /**
         * Deletes all known runnable commands.
         */
        void clearCommands() {
            return this->runnables_.clear();
        }

        /**
         * Returns all known runnable commands.
         *
         * @return KeyValueMap<uint8_t, AbstractCommand>
         */
        KeyValueMap<uint8_t, AbstractCommand *> getCommands() const {
            return this->runnables_;
        }

        /**
         * Add a runnable command to the known list.
         *
         * @param command AbstractCommand: a command.
         * @return bool: If the command as been stored properly.
         */
        bool addCommand(AbstractCommand *instance) {
            return this->runnables_.add(instance->getId(), instance);
        }

        /**
         * Gets a runnable command on the list by its ID.
         * @param id
         * @return AbstractCommand or NULL
         */
        AbstractCommand *getCommand(uint8_t id) {
            return this->runnables_.getValue(id);
        }

        /**
         * Stringifies the runnable command for debug purpose.
         *
         * @return String
         */
        operator String() {
            String log = "AbstractCommand Manager:\n";
            for (uint8_t i = 0; i < this->runnables_.count(); i++) {
                AbstractCommand *runnable = this->runnables_.get(i)->value;
                log += "# - " + String(*runnable) + "\n";
            }
            return log;
        }
};

#endif // ARDUINO_COMMAND_MANAGER_H
