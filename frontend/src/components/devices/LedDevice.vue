<template>
  <v-card width="400">
    <v-card-title>
      {{ device.name }}
      <v-spacer />
      <svg-led width="30" />
    </v-card-title>
    <v-card-subtitle>{{ board.name }} (PIN: {{ device.pin }})</v-card-subtitle>
    <v-card-text>
      <toggle-command v-model="device.value" :label="feedback" />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { defineModel } from "@/composables/vmodel";
import ToggleCommand from "@/components/commands/ToggleCommand.vue";
import { computed } from "vue";
import SvgLed from "@/components/icons/SvgLed.vue";
import { useBoardStore } from "@/stores/boards";

const props = defineProps({
  modelValue: Object
});
const device = defineModel(props);

// Get board.
const boardStore = useBoardStore();
const board = computed(() => boardStore.getBoard(props.modelValue!.board));

// Build toggle feedback label.
const feedback = computed(() => `Led: ${props.modelValue!.value === true ? "On" : "Off"}`);

</script>
