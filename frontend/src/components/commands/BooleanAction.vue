<template>
  <div
    :class="{'d-flex align-center command-compact': variant === 'compact'}"
    :title="infoComputed"
    class="command command-boolean"
  >
    <v-label class="command-label font-weight-bold">
      {{ labelComputed }}
    </v-label>
    <div class="command-pin ml-2 mr-2 text-lowercase font-italic d-none d-sm-block">
      ({{ $t("components.board.pin") }}: {{ command.pin }})
    </div>
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
  </div>
</template>

<script lang="ts" setup>
import { WritableComputedRef } from "vue";
import { useCommandStore } from "@/stores/commands";
import {
  CommandConfigurationProperties,
  useCommandFeedbackComputed,
  useCommandLabelComputed,
  useCommandTooltipComputed
} from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";

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

// Build label.
const labelComputed = useCommandLabelComputed(command.value, props);

// Build info (used when hover command).
const infoComputed = useCommandTooltipComputed(command.value, props);

// Build feedback label.
const feedbackComputed = useCommandFeedbackComputed(command.value, props);

// Send the command when the toggle changes.
const onChange = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
};

</script>

<style lang="scss" scoped>
.command {
  &-compact {
    .command-label {
      width: 7rem;
      text-overflow: ellipsis;
    }

    .command-pin {
      width: 4rem;
    }
  }
}
</style>