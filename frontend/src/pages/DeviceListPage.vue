<template>
  <component
    :is="useDevice(device.controller)"
    v-for="device in devices"
    :key="device.id"
    :device-id="device.id"
    class="ma-2"
  />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useDevice } from "@/composables/devices";
import { useDeviceStore } from "@/stores/devices";
import { useConfigStore } from "@/stores/config";

// Devices
const deviceStore = useDeviceStore();
const { devices } = storeToRefs(deviceStore);

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);
</script>
