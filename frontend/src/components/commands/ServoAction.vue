<template>
  <generic-action
    ref="action"
    v-model="command"
    :board="board"
    :variant="variant"
    class="command-servo"
  >
    <template #action>
      <v-slider
        v-if="isWideScreen"
        v-model="command.state"
        :label="feedbackComputed"
        :max="command.max"
        :min="command.min"
        :step="1"
        class="command-slider"
        color="primary"
        hide-details
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
            class="command-input pa-0"
            density="compact"
            hide-details
            single-line
            type="number"
            @change="setPosition"
          />
        </template>
      </v-slider>
      <v-text-field
        v-else
        v-model="position"
        :max="command.max"
        :min="command.min"
        class="command-input pa-0 flex-grow-0 d-block"
        density="compact"
        hide-details
        single-line
        type="number"
        @change="setPosition"
      />
    </template>
  </generic-action>
</template>

<script lang="ts" setup>
import { computed, ref, WritableComputedRef } from "vue";
import { useCommandStore } from "@/stores/commands";
import { defineModel } from "@/composables/vmodel";
import type { CommandConfigurationProperties } from "@/composables/commands";
import { useCommandFeedbackComputed } from "@/composables/commands";
import GenericAction from "@/components/commands/GenericAction.vue";
import { useElementSize } from "@vueuse/core";

type ServoCommandConfigurationProperties = CommandConfigurationProperties & {
  state: number
  min: number,
  max: number
  tmin?: number
  tmax?: number
}

const props = defineProps({
  variant: {
    type: String,
    default: "normal"
  },
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

const action = ref(null);
const { width } = useElementSize(action);
console.log(width);
const isWideScreen = computed(() => width.value > 500);

// Defines for v-model
const command: WritableComputedRef<ServoCommandConfigurationProperties> = defineModel(props);
const commandStore = useCommandStore();

const feedbackComputed = useCommandFeedbackComputed(command.value, props);

// Position is used as a v-model for the input number field and will then be merged back to the command model of the slider.
const position = ref(command.value.state);

// Send the command when the toggle changes.
// @todo Rework this method to use @end event when available with Vuetify 3.
// @see https://github.com/vuetifyjs/vuetify/issues/15675
const onSliderEnd = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (target?.className.includes("v-slider-")) {
    sendCommand();
  }
};

// Set the position to the slider (used when the input number text is updated).
const setPosition = (event: InputEvent) => {
  const target = event.target as HTMLInputElement;
  position.value = Math.min(command.value.max, Math.max(command.value.min, parseInt(target?.value)));
  command.value.state = position.value;
  sendCommand();
};

const sendCommand = () => {
  commandStore.sendCommand(props.board.id, command.value.id, command.value.state);
};

const decrement = () => {
  command.value.state = Math.max(command.value.min, --command.value.state);
  position.value = command.value.state;
  sendCommand();
};
const increment = () => {
  command.value.state = Math.min(command.value.max, ++command.value.state);
  position.value = command.value.state;
  sendCommand();
};

</script>

<style lang="scss">
.command-servo {
  &.command-compact {
    .command-input {
      width: 70px;

      input, .v-field__input {
        padding: 0 10px;
      }
    }
  }
}
</style>