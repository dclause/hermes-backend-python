<template>
  <v-card>
    <v-card-title class="d-flex">
      {{ board.name }}
      <v-spacer />
      <v-icon
        icon="mdi-multicast"
        width="30"
      />
    </v-card-title>
    <v-card-subtitle>
      <slot name="title">
        <div>Type: {{ board.model }}</div>
        <div>Status: {{ board.connected }}</div>
        <div>
          <component
            :is="useProtocol(board.protocol.controller)"
            :protocol="board.protocol"
          />
        </div>
      </slot>
    </v-card-subtitle>
    <v-card-text class="pa-0 pt-3">
      <v-expansion-panels
        multiple
        variant="accordion"
      >
        <v-expansion-panel elevation="0">
          <v-expansion-panel-title
            collapse-icon="mdi-minus"
            expand-icon="mdi-plus"
          >
            Actions
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <component
              :is="useDevice(device.controller)"
              v-for="(device, key) in board.actions"
              :key="key"
              v-model="board.actions[key]"
              :board="board"
              class="md-2"
              info=""
            />
          </v-expansion-panel-text>
        </v-expansion-panel>
        <v-expansion-panel elevation="0">
          <v-expansion-panel-title
            collapse-icon="mdi-minus"
            expand-icon="mdi-plus"
          >
            Inputs
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <em>No input for this board.</em>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { useBoardStore } from "@/stores/boards";
import { useDevice } from "@/composables/devices";
import { useProtocol } from "@/composables/protocols";

const props = defineProps({
  boardId: {
    type: Number,
    required: true
  }
});

const boardStore = useBoardStore();
const board = boardStore.getBoard(props.boardId);
</script>


<style lang="scss" scoped>
.v-card-subtitle {
  display: block;
}
</style>