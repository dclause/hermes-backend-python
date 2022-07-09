<template>
  <v-card width="400">
    <v-card-title>
      {{ device.name }}
      <v-spacer />
      <svg-led width="30" />
    </v-card-title>
    <v-card-subtitle>{{ board.name }} (PIN: {{ device.pin }})</v-card-subtitle>
    <v-card-text>
      <toggle-command
        v-model="device"
        :label="feedback"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import ToggleCommand from "@/components/commands/ToggleCommand.vue";
import { computed } from "vue";
import SvgLed from "@/components/icons/SvgLed.vue";
import { useBoardStore } from "@/stores/boards";
import { DeviceConfigurationProperties, useDeviceStore } from "@/stores/devices";

const props = defineProps({
  deviceId: {
    type: Number,
    required: true
  }
});

// Get device.
const deviceStore = useDeviceStore();
const device: DeviceConfigurationProperties = deviceStore.getDevice(
  props.deviceId
);

// Get board.
const boardStore = useBoardStore();
const board = computed(() => boardStore.getBoard(device.board));

// Build toggle feedback label.
const feedback = computed(() => `Led: ${device.value === true ? "On" : "Off"}`);

</script>
