<template>
  <div class="command command-boolean">
    <v-label class="text-body-2 font-weight-bold">
      Command "{{ command.name }}" :
    </v-label>
    <v-switch
      v-model="command.state"
      :label="labelComputed"
      color="primary"
      hide-details
      inline
      inset
      density="compact"
      @change="onChange"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, WritableComputedRef } from "vue";
import { useSocket } from "@/plugins/socketIO";
import { defineModel } from "@/composables/vmodel";
import { CommandConfigurationProperties } from "@/composables/commands";

const socket = useSocket();

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  device: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    default: ""
  }
});

// Defines for v-model
const command: WritableComputedRef<CommandConfigurationProperties> = defineModel(props);


// Build feedback label.
const labelComputed = computed(() => {
  if (props.label) {
    return props.label;
  }
  if (command.value.name) {
    return `${command.value.name} on PIN ${command.value.pin}: ${command.value.state === true ? "On" : "Off"}`;
  }
  return `PIN ${command.value.pin}: ${command.value.state === true ? "On" : "Off"}`;
});

/**
 * Forward the command via the backend socketIO connexion to the robot.
 * @see backend/hermes/core/server.py
 */
// @todo run a store action to emit the command so others can subscribe to it.
const onChange = () => {
  console.debug("BooleanAction: value is now ", command.value.state);
  socket.emit("action", props.device.id, command.value.id, command.value.state);
};

</script>

<style lang="scss">
.command {
  .v-label {
    font-size: 0.9rem;
  }

  .v-selection-control {
    height: auto;
  }
}
</style>