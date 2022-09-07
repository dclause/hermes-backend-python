<template>
  <generic-device
    v-model="device"
    :board="board"
    :variant="variant"
    class="command command-led"
  >
    <template #icon>
      <svg-led
        class="ml-2 mr-3"
        width="30"
      />
    </template>
    <template #command>
      <boolean-action
        v-model="device"
        :board="board"
        class="flex-grow-1"
        variant="compact"
      />
    </template>
  </generic-device>
</template>

<script lang="ts" setup>
import { WritableComputedRef } from "vue";
import SvgLed from "@/components/icons/SvgLed.vue";
import BooleanAction from "@/components/commands/BooleanAction.vue";
import type { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import GenericDevice from "@/components/devices/GenericDevice.vue";

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
