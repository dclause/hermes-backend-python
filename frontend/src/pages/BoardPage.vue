<template>
  <div class="d-flex justify-space-between align-center mb-4">
    <h1 class="d-inline-block text-h5 text-md-h4">
      {{ board.name }}
    </h1>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { useBoardStore } from "@/stores/boards";

const route = useRoute();
const boardId: number = Number.parseInt(route.params.boardId as string);

const boardStore = useBoardStore();
const board = boardStore.getBoard(boardId);

</script>

<style lang="scss" scoped>

.board-list {
  .col-icon,
  .col-status {
    width: 30px;
    text-align: center;
  }
}

</style>
