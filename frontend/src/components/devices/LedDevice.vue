<template>
  <v-card width="calc(33.33% - 16px)">
    <v-card-title>
      {{ device.name }}
      <v-spacer />
      <svg-led width="30" />
    </v-card-title>
    <v-card-subtitle>{{ board.name }}</v-card-subtitle>
    <v-card-text>
      <boolean-action
        v-model="device.actions[0]"
        :device="device"
        :label="feedback"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import SvgLed from "@/components/icons/SvgLed.vue";
import { useBoardStore } from "@/stores/boards";
import { useDeviceStore } from "@/stores/devices";
import { DeviceConfigurationProperties } from "@/composables/devices";
import BooleanAction from "@/components/commands/BooleanAction.vue";
import { CommandConfigurationProperties } from "@/composables/commands";

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

// Get command.
const command: CommandConfigurationProperties = device.actions[0];

// Build toggle feedback label.
const feedback = computed(() => `Led: ${command.state === true ? "On" : "Off"}`);

</script>
