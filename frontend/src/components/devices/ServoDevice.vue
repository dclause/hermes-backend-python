<template>
  <generic-device
    v-model="device"
    :board="board"
    :variant="variant"
    class="command command-servo"
  >
    <template #icon>
      <svg-servo
        class="ml-2 mr-3"
        width="30"
      />
    </template>
    <template #command>
      <servo-action
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
import { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import ServoAction from "@/components/commands/ServoAction.vue";
import SvgServo from "@/components/icons/SvgServo.vue";
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