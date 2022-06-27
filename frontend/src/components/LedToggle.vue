<template>
  <v-switch
    v-model="led"
    :label="`Switch: ${led.toString()}`"
    color="primary"
    hide-details
    inline
    inset
  ></v-switch>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useLedStore } from "@/stores/led";

const ledStore = useLedStore();
const { led } = storeToRefs(ledStore);
</script>
