<template>
  <!-- Compact variant -->
  <div
    v-if="variant === 'compact'"
    class="d-flex mt-2 mb-2"
  >
    <slot name="icon">
      <v-icon
        icon="mdi-progress-question"
        width="30"
      />
    </slot>

    <slot name="command">
      <unknown-command />
    </slot>
    <v-btn
      icon="mdi-dots-vertical"
      variant="plain"
    />
  </div>

  <!-- Normal variant -->
  <v-card v-else>
    <v-card-title class="d-flex">
      {{ device.name }}
      <v-spacer />
      <slot name="icon">
        <v-icon
          icon="mdi-progress-question"
          width="30"
        />
      </slot>
    </v-card-title>
    <v-card-subtitle>{{ board.name }}</v-card-subtitle>
    <v-card-text>
      <slot name="action">
        <unknown-command />
      </slot>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { WritableComputedRef } from "vue";
import type { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import UnknownCommand from "@/components/commands/UnknownCommand.vue";

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
  }
});

// Define for v-model
const device: WritableComputedRef<CommandConfigurationProperties> = defineModel(props);
</script>