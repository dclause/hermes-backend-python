<template>
  <custom-board board-id="boardId">
    <template #title>
      <div>{{ $t("components.board.type") }}: {{ board.model }}</div>
      <div>{{ $t("components.board.type") }}: {{ board.connected }}</div>
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
