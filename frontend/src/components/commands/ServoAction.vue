<template>
  <div
    :title="infoComputed"
    class="command command-servo"
  >
    <v-label class="text-body-2 font-weight-bold">
      {{ labelComputed }}
    </v-label>

    <v-slider
      v-model="command.state"
      :label="feedbackComputed"
      :max="command.max"
      :min="command.min"
      :step="1"
      color="primary"
      track-color="grey"
      @mouseup="onSliderEnd"
      @update:model-value="position = command.state"
    >
      <template #prepend>
        <v-btn
          icon="mdi-minus"
          size="small"
          variant="text"
          @click="decrement"
        />
      </template>

      <template #append>
        <v-btn
          icon="mdi-plus"
          size="small"
          variant="text"
          @click="increment"
        />
        <v-text-field
          v-model="position"
          :max="command.max"
          :min="command.min"
          density="compact"
          hide-details
          single-line
          style="width: 100px"
          type="number"
          @change="setPosition"
        />
      </template>
    </v-slider>
  </div>
</template>

<script lang="ts" setup>
import { computed, WritableComputedRef } from "vue";
import { useCommandStore } from "@/stores/commands";
import { defineModel } from "@/composables/vmodel";
import {
  CommandConfigurationProperties,
  useCommandFeedbackComputed,
  useCommandInfoComputed,
  useCommandLabelComputed
} from "@/composables/commands";

type ServoCommandConfigurationProperties = CommandConfigurationProperties & {
  state: number
  min: number,
  max: number
  tmin?: number
  tmax?: number
}

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  board: {
    type: Object,
    required: true
  },
  label: {
    type: String,
    default: undefined
  },
  info: {
    type: String,
    default: undefined
  },
  feedback: {
    type: String,
    default: undefined
  }
});

// Defines for v-model
const command: WritableComputedRef<ServoCommandConfigurationProperties> = defineModel(props);
const commandStore = useCommandStore();

const labelComputed = useCommandLabelComputed(command.value, props);
const infoComputed = useCommandInfoComputed(command.value, props);
const feedbackComputed = useCommandFeedbackComputed(command.value, props);

// Position is used as a v-model for the input number field and will then be merged back to the command model
// of the slider.
const position = computed(() => command.value.state);

// Send the command when the toggle changes.
// @todo Rework this method to use @end event when available with Vuetify 3.
const onSliderEnd = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (target?.className.includes("v-slider-")) {
    sendCommand();
  }
};

// Set the position to the slider (used when the input number text is updated).
const setPosition = (event: InputEvent) => {
  const target = event.target as HTMLInputElement;
  command.value.state = Math.min(command.value.max, Math.max(command.value.min, parseInt(target?.value)));
  sendCommand();
};

const sendCommand = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
};

const decrement = () => {
  command.value.state--;
  sendCommand();
};
const increment = () => {
  command.value.state++;
  sendCommand();
};

</script>

<style lang="scss" scoped>
.command {
  .v-label {
    font-size: 0.9rem;
  }
}
</style>