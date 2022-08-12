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
import {
  CommandConfigurationProperties,
  useCommandFeedbackComputed,
  useCommandInfoComputed
} from "@/composables/commands";
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

// Build info (used when hover command).
const infoComputed = useCommandInfoComputed(command.value, props);

// Build feedback label.
const feedbackComputed = useCommandFeedbackComputed(command.value, props);

// Send the command when the toggle changes.
const onChange = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
};

</script>

<style lang="scss" scoped>
.command {
  .v-label {
    font-size: 0.9rem;
  }

  .v-selection-control {
    height: auto;
  }
}
</style>