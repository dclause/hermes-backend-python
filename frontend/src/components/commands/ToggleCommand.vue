<template>
  <v-switch
    v-model="device.state"
    :label="label"
    color="primary"
    hide-details
    inline
    inset
    @change="onChange"
  />
</template>

<script lang="ts" setup>
import { defineModel } from "@/composables/vmodel";
import { useCommand } from "@/composables/commands";
import { WritableComputedRef } from "vue";
import { useSocket } from "@/plugins/socketIO";
import { DeviceConfigurationProperties } from "@/stores/devices";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    default: ""
  }
});

const device: WritableComputedRef<DeviceConfigurationProperties> = defineModel(props);
const socket = useSocket();

// watch(() => props.modelValue.state, (newValue, oldValue) => {
//   console.log(
//     "Watch led value function called with args:",
//     newValue,
//     oldValue
//   );
//   socket.emit("command", useCommand.ON_OFF, device.value.id, newValue);
// });

const onChange = () => {
  console.log(
    "onChange led value function called with args:",
    device.value.state
  );
  socket.emit("command", useCommand.ON_OFF, device.value.id, device.value.state);
};

</script>
