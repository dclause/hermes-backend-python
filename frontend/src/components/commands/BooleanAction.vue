<template>
  <div
    class="command command-boolean"
    :title="infoComputed"
  >
    <v-label class="text-body-2 font-weight-bold">
      {{ labelComputed }}
    </v-label>
    <v-switch
      v-model="command.state"
      :label="feedbackComputed"
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
import { useCommandStore } from "@/stores/commands";
import { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  board: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    default: undefined
  },
  info: {
    type: String,
    default: undefined
  },
  feedback: {
    type: String,
    default: undefined
  }
});

// Defines for v-model
const command: WritableComputedRef<CommandConfigurationProperties> = defineModel(props);
const commandStore = useCommandStore();

// Build label.
const labelComputed = computed(() => {
  if (props.label !== undefined) {
    return props.label;
  }
  return `Command "${command.value.name}" :`;
});

// Build info.
const infoComputed = computed(() => {
  if (props.info !== undefined) {
    return props.info;
  }
  return `Board "${props.board.name}" (PIN ${command.value.pin}): ${command.value.state === true ? "On" : "Off"}`;
});

// Build feedback label.
const feedbackComputed = computed(() => {
  if (props.feedback !== undefined) {
    return props.feedback;
  }
  return `PIN ${command.value.pin}: ${command.value.state === true ? "On" : "Off"}`;
});

// Send the command when the toggle changes.
const onChange = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
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