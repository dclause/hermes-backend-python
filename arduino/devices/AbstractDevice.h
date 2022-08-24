#ifndef ARDUINO_DEVICE_H
#define ARDUINO_DEVICE_H

#include "../helper/debugger.h"
#include "../helper/ioserial.h"
#include <Arduino.h>


/**
 * Class AbstractDevice: all devices must implement this class.
 * @see DeviceManager.h
 */
class AbstractDevice {
    protected:
        uint8_t id_ = 0;
        int expected_payload_size_;
        uint8_t effective_payload_size_;
        uint8_t *payload_;

    public:

        AbstractDevice(const int expected_payload_size = 0) :
                expected_payload_size_(expected_payload_size),
                effective_payload_size_(expected_payload_size ? expected_payload_size : 0) {
            if (expected_payload_size > 0) {
                this->payload_ = new uint8_t[expected_payload_size];
            } else {
                // Size indicator in messages is on 8bits, hence the 255 max size when size is unknown.
                this->payload_ = new uint8_t[255];
            }
        }

        virtual ~AbstractDevice() {
            free(this->payload_);
            this->payload_ = NULL;
        };

        /**
         * Returns a human readable name for the device.
         *
         * @return String
         */
        virtual String getName() const = 0;

        /**
         * Returns the ID of this device.
         * We use a getter to the protected id_ attribute to make sure no-one changes this from the outside.
         * The only way to change the ID is via the updateFromPayload() method which ensures the ID can't be changed
         * afterward.
         *
         * @return String
         */
        uint8_t getId() const { return this->id_; };

        /**
         * Update the internal settings of a device from a bytes payload.
         *
         * @note This situation occurs when a handshake is made and the actions/inputs are declared by the backend to
         * the board (@see HandshakeCommand) or when an action/input is updated (for instance the servo speed is changed).
         *
         * @note The implementation below is pretty light. But as an AbstractDevice, we only know that payload[0] is the
         * the device id. Every implementation is responsible to override this method and know what the payload contains
         * for itself.
         *
         * @param payload
         */
        virtual void updateFromPayload(const uint8_t *payload) {
            if (this->id_ == 0) {
                this->id_ = payload[0];
            }
        }

        /**
         * Update the device internal state depending on time of the nextTick.
         */
        virtual void nextTick() {};

        /**
         * Processes the device when received from the serial port. That means receive the payload and execute it.
         */
        void process() {
            this->receivePayload_();
            this->executePayload(this->payload_);
        };

        /**
         * Executes the device using the given payload.
         *
         * @param payload (uint8_t*)
         */
        virtual void executePayload(uint8_t *payload) = 0;

        /**
         * Stringifies the device for debug purpose.
         *
         * @return String
         */
        operator String() const {
            return "Command (" + String(this->getId()) + ") " + this->getName() + " ";
        }

    private:

        /**
         * Load the expected data in the internal payload.
         * The amount of data loaded is defined by the expected_payload_size_ variable for the device, or the given data
         * size as first byte sent after device code.
         * ex: 33 26 1 2 3 .... 26 would solve to a HANDSHAKE (33) with 26 bytes or data (1...26)
         *
         * The maximum amount of data sent is 255 bytes.
         */
        void receivePayload_() {

            // When the payload size can vary (negative expected_payload_size), the first byte receive
            // is the effective size of the incoming payload.
            if (this->expected_payload_size_ < 0) {
                IO::wait_for_bytes(1);
                IO::read_bytes(this->payload_, 1);
                this->effective_payload_size_ = this->payload_[0];
            } else {
                this->effective_payload_size_ = this->expected_payload_size_;
            }

            if (this->effective_payload_size_ > 0) {
                IO::wait_for_bytes(this->effective_payload_size_);
                IO::read_bytes(this->payload_, this->effective_payload_size_);
            }
            TRACE("Payload size: " + String(this->effective_payload_size_));
#ifdef TRACE
            String payloadAsInts = "";
            for (uint8_t i = 0; i < this->effective_payload_size_; i++) {
                payloadAsInts += String(this->payload_[i]) + " ";
            }
            TRACE("Payload received: " + payloadAsInts);
#endif
        }
};

#endif// ARDUINO_DEVICE_H
