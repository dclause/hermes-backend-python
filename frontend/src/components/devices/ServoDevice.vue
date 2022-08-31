<template>
  <!-- Compact variant -->
  <div
    v-if="variant === 'compact'"
    class="d-flex mt-2 mb-2"
  >
    <v-tooltip
      v-model="tooltip"
      location="bottom"
    >
      <template #activator="{ on, attrs }">
        <svg-servo
          :class="{'ml-2 mr-3': variant === 'compact'}"
          v-bind="attrs"
          width="30"
          @click="tooltip = !tooltip"
        />
      </template>
      <span>{{ device.name }}</span>
    </v-tooltip>


    <servo-action
      v-model="device"
      :board="board"
      class="flex-grow-1"
      variant="compact"
    />
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
      <svg-servo width="30" />
    </v-card-title>
    <v-card-subtitle>{{ board.name }}</v-card-subtitle>
    <v-card-text>
      <servo-action
        v-model="device"
        :board="board"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { ref, WritableComputedRef } from "vue";
import { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import ServoAction from "@/components/commands/ServoAction.vue";
import SvgServo from "@/components/icons/SvgServo.vue";

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
const tooltip = ref(false);
</script>