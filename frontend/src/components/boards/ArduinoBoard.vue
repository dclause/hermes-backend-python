<template>
  <v-card width="400">
    <v-card-title>
      {{ board.name }}
      <v-spacer />
      <svg-arduino width="40" />
    </v-card-title>
    <v-card-subtitle>Type: {{ board.model }}</v-card-subtitle>
    <v-card-subtitle>Port: {{ board.port }}</v-card-subtitle>
    <v-card-subtitle>Status: {{ board.connected }}</v-card-subtitle>
  </v-card>
</template>

<script lang="ts" setup>
import SvgArduino from "@/components/icons/SvgArduino.vue";
import { useBoardStore } from "@/stores/boards";

const props = defineProps({
  boardId: {
    type: String,
    required: true
  }
});

const boardStore = useBoardStore();
const board = boardStore.getBoard(props.boardId);
</script>
