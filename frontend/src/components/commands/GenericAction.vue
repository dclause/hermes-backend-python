<template>
  <div
    ref="action"
    :class="{'d-flex flex-grow-1 align-center command-compact': variant === 'compact'}"
    :title="infoComputed"
    class="command command-boolean"
  >
    <v-label class="command-label font-weight-bold">
      {{ labelComputed }}
    </v-label>
    <div
      v-if="isWideScreen"
      class="command-pin ml-2 mr-2 text-lowercase font-italic"
    >
      ({{ $t("components.board.pin") }}: {{ command.pin }})
    </div>
    <slot name="action">
      <unknown-command />
    </slot>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, WritableComputedRef } from "vue";
import {
  CommandConfigurationProperties,
  useCommandLabelComputed,
  useCommandTooltipComputed
} from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import UnknownCommand from "@/components/commands/UnknownCommand.vue";
import { useElementSize } from "@vueuse/core";

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

const action = ref(null);
const { width } = useElementSize(action);
const isWideScreen = computed(() => width.value > 600);

// Define for v-model
const command: WritableComputedRef<CommandConfigurationProperties> = defineModel(props);

// Build label.
const labelComputed = useCommandLabelComputed(command.value, props);

// Build info (used when hover command).
const infoComputed = useCommandTooltipComputed(command.value, props);

</script>

<style lang="scss" scoped>
@import 'vuetify/lib/styles/settings/variables';

.command {
  &-compact {
    .command-label {
      width: 7rem;
      text-overflow: ellipsis;
      display: block;
    }

    .command-pin {
      width: 4rem;
    }
  }
}
</style>