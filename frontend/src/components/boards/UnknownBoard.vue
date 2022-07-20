<template>
  <v-card width="400">
    <v-card-title>
      {{ board.name }}
      <v-spacer />
      <v-icon
        icon="mdi-multicast"
        width="30"
      />
    </v-card-title>
    <v-card-subtitle>Type: {{ board.model }}</v-card-subtitle>
    <v-card-subtitle>Status: {{ board.connected }}</v-card-subtitle>
  </v-card>
</template>

<script lang="ts" setup>
import { useBoardStore } from "@/stores/boards";

const props = defineProps({
  boardId: {
    type: Number,
    required: true
  }
});

const boardStore = useBoardStore();
const board = boardStore.getBoard(props.boardId);
</script>
