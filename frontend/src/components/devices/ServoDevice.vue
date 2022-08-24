<template>
  <v-card>
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
import { WritableComputedRef } from "vue";
import { CommandConfigurationProperties } from "@/composables/commands";
import { defineModel } from "@/composables/vmodel";
import ServoAction from "@/components/commands/ServoAction.vue";
import SvgServo from "@/components/icons/SvgServo.vue";

const props = defineProps({
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