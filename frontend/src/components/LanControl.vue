<!--
Monitors the socketIO connection to the server.
-->

<template>
  <v-tooltip location="bottom">
    <template v-slot:activator="{ props }">
      <v-btn :class="status.class" :icon="status.icon" v-bind="props" />
    </template>
    <span>{{ status.status }}</span>
  </v-tooltip>
</template>

<script lang="ts" setup>
import { useSocket } from "@/plugins/socketIO";
import { useLedStore } from "@/stores/led";
import { MutationType } from "pinia";
import { reactive } from "vue";

// Extract composables.
const ledStore = useLedStore();
const socket = useSocket();

// Init the status display.
const status = reactive({
  icon: "mdi-lan-pending",
  class: "blink",
  status: "connecting",
});

// Defines socket receivable messages.
socket
  .on("connect", () => {
    status.icon = "mdi-lan-check";
    status.class = "";
    status.status = "connected";
  })
  .on("reconnect_attempt", () => {
    console.log("attempt reconnect");
    status.icon = "mdi-lan-pending";
    status.class = "blink";
    status.status = "connecting";
  })
  .on("disconnect", () => {
    status.icon = "mdi-lan-disconnect";
    status.class = "";
    status.status = "disconnected";
  })
  .on("patch", (paylaod) => {
    console.log("patch event received:", paylaod);
    ledStore.$state = paylaod;
  });

// Subscribe to the ledStore: when anything within changes, notify the backend
// to broadcast this.
ledStore.$subscribe((mutation, state) => {
  console.log("## led store has mutated ##", mutation.type, state);
  if (mutation.type == MutationType.direct) {
    console.log("## emit mutation ##");
    socket.emit("mutation", state);
  }
});
</script>

<style lang="css">
@keyframes blink {
  50% {
    opacity: 0.5;
  }
}

.blink {
  animation: blink 0.5s step-start 0s infinite;
}
</style>
