<template>
  <custom-board board-id="boardId">
    <template #title>
      <div>Type: {{ board.model }}</div>
      <div>Status: {{ board.connected }}</div>
    </template>
  </custom-board>
</template>

<script lang="ts" setup>
import { useBoardStore } from "@/stores/boards";
import CustomBoard from "@/components/boards/CustomBoard.vue";

const props = defineProps({
  boardId: {
    type: Number,
    required: true
  }
});

const boardStore = useBoardStore();
const board = boardStore.getBoard(props.boardId);
</script>
