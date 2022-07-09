<template>
  <v-container v-if="connected">
    <component
      :is="useDevice(device.type)"
      v-for="device in devices"
      :key="device.id"
      :device-id="device.id"
    />
  </v-container>
  <lan-broken v-else />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useDevice } from "@/composables/devices";
import { useDeviceStore } from "@/stores/devices";
import LanBroken from "@/components/connexion/LanBroken.vue";
import { useConfigStore } from "@/stores/config";

// Devices
const deviceStore = useDeviceStore();
const { devices } = storeToRefs(deviceStore);

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);
</script>
