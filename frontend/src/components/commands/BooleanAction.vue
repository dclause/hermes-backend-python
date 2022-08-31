<template>
  <generic-action
    v-model="command"
    :board="board"
    :variant="variant"
  >
    <template #action>
      <v-switch
        v-model="command.state"
        :label="feedbackComputed"
        class="ml-5"
        color="primary"
        density="compact"
        hide-details
        inline
        inset
        @change="onChange"
      />
    </template>
  </generic-action>
</template>

<script lang="ts" setup>
import { WritableComputedRef } from "vue";
import { useCommandStore } from "@/stores/commands";
import { CommandConfigurationProperties, useCommandFeedbackComputed } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import GenericAction from "@/components/commands/GenericAction.vue";

const props = defineProps({
  variant: {
    type: String,
    default: "normal"
  },
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

const commandStore = useCommandStore();

// Define for v-model
const command: WritableComputedRef<CommandConfigurationProperties> = defineModel(props);

// Build feedback label.
const feedbackComputed = useCommandFeedbackComputed(command.value, props);

// Send the command when the toggle changes.
const onChange = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
};

</script>