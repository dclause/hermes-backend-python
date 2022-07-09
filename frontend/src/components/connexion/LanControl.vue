<template>
  <v-tooltip location="bottom">
    <template #activator="{ props }">
      <v-btn
        :class="{ blink: pending }"
        :icon="icon"
        v-bind="props"
      />
    </template>
    <span>Server: {{ status }}</span>
  </v-tooltip>
</template>

<script lang="ts" setup>
import { useSocket } from "@/plugins/socketIO";
import { useLedStore } from "@/stores/led";
import { MutationType, storeToRefs } from "pinia";
import { computed } from "vue";
import { useConfigStore } from "@/stores/config";
import { useProfileStore } from "@/stores/profile";
import { useBoardStore } from "@/stores/boards";
import { useDeviceStore } from "@/stores/devices";

// Extract composable.
const ledStore = useLedStore();
const configStore = useConfigStore();
const profileStore = useProfileStore();
const boardStore = useBoardStore();
const deviceStore = useDeviceStore();
const socket = useSocket();

const { connected } = storeToRefs(configStore);
const pending = computed(() => connected.value === undefined);

const icon = computed(() => {
  if (pending.value) {
    return "mdi-lan-pending";
  } else if (connected.value) {
    return "mdi-lan-check";
  }
  return "mdi-lan-disconnect";
});

const status = computed(() => {
  if (pending.value) {
    return "connecting...";
  } else if (connected.value) {
    return "connected";
  }
  return "disconnected";
});

// Defines socket receivable messages.
socket
  .on("connect", () => {
    configStore.$patch({ connected: true });
  })
  .on("reconnect_attempt", () => {
    console.log("attempt reconnect");
    configStore.$patch({ connected: undefined });
  })
  .on("handshake", (global, profile, boards, devices) => {
    console.log("Handshake received");
    configStore.$state = global;
    profileStore.$state = profile;
    boardStore.$patch({ boards: boards });
    deviceStore.$patch({ devices: devices });
  })
  .on("disconnect", () => {
    configStore.$patch({ connected: false });
  })
  .on("patch", (paylaod) => {
    console.log("patch event received:", paylaod);
    ledStore.$state = paylaod;
  });

// Subscribe to the ledStore: when anything within changes, notify the backend
// to broadcast this.
// @todo remove this
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
