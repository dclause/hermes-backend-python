#ifndef ARDUINO_MAP_H
#define ARDUINO_MAP_H

#include <Arduino.h>

/**
 * Defines an associative key/value element to be used in KeyValueMap.
 *
 * @tparam Key      the key element type (ex. int, string, etc...)
 * @tparam Value    the value element type (ex. Command, AbstractDevice, etc...)
 */
template<typename Key, typename Value>
class Pair {
    public:
        const Key key;
        const Value value;
        Pair<Key, Value> *next;

        Pair() {}

        Pair(Key key, Value value) : key(key), value(value), next(NULL) {}

        operator String() {
            return (String) this->key + F(" - ") + (String) this->value;
        }
};

/**
 * Defines a FIFO-type chained list of associative key/value pairs.
 *
 * @tparam Key      the key element type (ex. int, string, etc...)
 * @tparam Value    the value element type (ex. Command, AbstractDevice, etc...)
 */
template<typename Key, typename Value>
class KeyValueMap {
    public:
        KeyValueMap() : head_(NULL), size_((uint8_t) 0) {}

        ~KeyValueMap() { this->clear(); }

        uint8_t count() {
            return this->size_;
        }

        /**
         * Deletes all elements in the list.
         */
        void clear() {
            Pair<Key, Value> *node = this->head_;
            while (this->head_) {
                this->head_ = this->head_->next;
                delete node;
                node = this->head_;
            }
            this->size_ = 0;
        }

        /**
         * Adds an element at the head of the list.
         *
         * @warning
         * If an element with the same key exists, the addition is rejected and the return is `false`.
         *
         * @param key (Key)
         * @param value
         * @return bool If the element has been added to the list.
         */
        bool add(const Key key, const Value value) {
            if (this->getPosition(key) != -1) {
                return false;
            }
            Pair<Key, Value> *node = new Pair<Key, Value>(key, value);
            node->next = this->head_;
            this->head_ = node;
            this->size_ += 1;
            return true;
        }

        /**
         * Removes an element from the list.
         *
         * @param key
         * @return bool If the element has been removed from the list.
         */
        bool remove(Key key) {
            Pair<Key, Value> *current = this->head_;
            while (current) {
                if (current->next->key == key) {
                    break;
                }
                current = current->next;
            }
            if (current) {
                Pair<Key, Value> *toBeDeleted = current->next;
                current->next = toBeDeleted->next;
                this->size_ -= 1;
                delete toBeDeleted;
                return true;
            }
            return false;
        }

        /**
         * Returns the element which index is `key`.
         * Overrides get operator using the [] syntax.
         *
         * @example
         *      Value value = my_list[my_key];`
         *
         * @param key
         * @return The element or NULL.
         */
        Pair<Key, Value> *operator[](Key key) {
            Pair<Key, Value> *current = this->head_;
            while (current) {
                if (current->key == key) {
                    return current;
                }
                current = current->next;
            }
            return NULL;
        }

        /**
         * Returns the element which index is `key`.
         * Overrides get operator using the [] syntax.
         *
         * @note
         * This method is identical to using the map[key] operator.
         *
         * @example
         *      Value value = my_list[my_key];`
         *
         * @param key
         * @return The element or NULL.
         */
        Value getValue(Key const key) {
            return (*this)[key]->value;
        }

        /**
         * Returns the element at i-th position.
         *
         * @param key
         * @return The pair or NULL.
         */
        Pair<Key, Value> *get(uint8_t position) {
            if (position < 0 || position >= this->size_) {
                return NULL;
            }
            Pair<Key, Value> *current = this->head_;
            for (uint8_t i = 0; i < position; i++) {
                current = current->next;
            }
            return current;
        }

        /**
         * Gets the position of the element with the given key.
         *
         * @param key
         * @return the position, or `-1` if not found.
         */
        int getPosition(Key const key) {
            Pair<Key, Value> *current = this->head_;
            for (uint8_t i = 0; i < this->size_; i++) {
                if (current->key == key) {
                    return i;
                }
                current = current->next;
            }
            return -1;
        }

        /**
         * Converts to string for debug purpose.
         *
         * @return String
         */
        operator String() {
            String output = (String) F("Debug map (") + this->count() + (String) F(" elements):\n");
            Pair<Key, Value> *current = this->head_;
            for (uint8_t i = 0; i < this->size_; i++) {
                output += (String) F("  > ") + (String) (*current) + '\n';
                current = current->next;
            }
            return output;
        }

    private:
        Pair<Key, Value> *head_ = NULL;
        uint8_t size_ = 0;
};

#endif // ARDUINO_MAP_H
