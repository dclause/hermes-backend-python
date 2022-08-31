<template>
  <div
    :class="{'d-flex align-center command-compact': variant === 'compact'}"
    :title="infoComputed"
    class="command command-servo"
  >
    <v-label class="command-label font-weight-bold">
      {{ labelComputed }}
    </v-label>
    <div class="command-pin ml-2 mr-2 text-lowercase font-italic d-none d-sm-block">
      ({{ $t("components.board.pin") }}: {{ command.pin }})
    </div>
    <v-slider
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
          class="command-input"
          density="compact"
          hide-details
          single-line
          style="width: 100px"
          type="number"
          @change="setPosition"
        />
      </template>
    </v-slider>
    <v-text-field
      v-model="position"
      :max="command.max"
      :min="command.min"
      class="command-input flex-grow-0 d-block d-md-none"
      density="compact"
      hide-details
      single-line
      type="number"
      @change="setPosition"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, WritableComputedRef } from "vue";
import { useCommandStore } from "@/stores/commands";
import { defineModel } from "@/composables/vmodel";
import {
  CommandConfigurationProperties,
  useCommandFeedbackComputed,
  useCommandLabelComputed,
  useCommandTooltipComputed
} from "@/composables/commands";

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

// Defines for v-model
const command: WritableComputedRef<ServoCommandConfigurationProperties> = defineModel(props);
const commandStore = useCommandStore();

const labelComputed = useCommandLabelComputed(command.value, props);
const infoComputed = useCommandTooltipComputed(command.value, props);
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

<style lang="scss" scoped>
@import 'vuetify/lib/styles/settings/variables';

.command {
  &-compact {
    .command-label {
      width: 7rem;
      text-overflow: ellipsis;
    }

    .command-pin {
      width: 4rem;
    }

    .command-slider {
      display: none;
    }

    .command-input {
      width: 100px;
    }

    @media #{map-get($display-breakpoints, 'md-and-up')} {
      .command-slider {
        display: grid;
      }
    }
  }
}
</style>