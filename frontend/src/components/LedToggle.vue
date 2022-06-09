<template>
  <v-switch
    v-model="led"
    :label="`Switch: ${led.toString()}`"
    color="primary"
    hide-details
    inset
  ></v-switch>
</template>

<script lang="ts" setup>
import { useLedStore } from "@/stores/led";
import { storeToRefs } from "pinia";
import { useSocketIO } from "@/plugins/socketIO";

const { socket } = useSocketIO();

const ledStore = useLedStore();

const { led } = storeToRefs(ledStore);

ledStore.$subscribe((mutation, state) => {
  console.log("## led store has mutated ##", state);
  socket.emit("mutation", state);
});

socket.onAny((eventName, ...args) => {
  console.log("event received:", eventName, args);
});
</script>
