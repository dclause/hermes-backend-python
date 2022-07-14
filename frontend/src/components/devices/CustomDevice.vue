<template>
  <v-card width="400">
    <v-card-title>
      {{ device.name }}
      <v-spacer />
      <v-icon
        icon="mdi-progress-question"
        width="30"
      />
    </v-card-title>
    <v-card-subtitle>{{ board.name }}</v-card-subtitle>
    <v-card-text>
      <component
        :is="useCommand(command.type)"
        v-for="(command, key) in device.commands"
        :key="key"
        v-model="device.commands[key]"
        class="md-2"
        :device-id="device.id"
      />
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import { useBoardStore } from "@/stores/boards";
import { useDeviceStore } from "@/stores/devices";
import { useCommand } from "@/composables/commands";
import { DeviceConfigurationProperties } from "@/composables/devices";

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

</script>
