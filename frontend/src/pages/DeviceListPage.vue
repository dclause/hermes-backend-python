<template>
  <component :is="useDevice(device.type)" v-for="(device, id) in devices" :key="device.id" v-model="devices[id]" />
  <lan-broken v-if="!hasDevices" />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useDevice } from "@/composables/devices";
import { useDeviceStore } from "@/stores/devices";
import LanBroken from "@/components/connexion/LanBroken.vue";

const deviceStore = useDeviceStore();
const { devices } = storeToRefs(deviceStore);
const hasDevices = !!Object.keys(devices).length;
</script>
