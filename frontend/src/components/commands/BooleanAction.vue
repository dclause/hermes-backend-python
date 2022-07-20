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
import { defineModel } from "@/composables/vmodel";
import { CommandConfigurationProperties } from "@/composables/commands";
import { useCommandStore } from "@/stores/commands";

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
const commandStore = useCommandStore();

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

// Send the command when the toggle changes.
const onChange = () => {
  commandStore.sendCommand(props.device.id, command.value.id, command.value.state);
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