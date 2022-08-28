<template>
  Hello board
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useBoardStore } from "@/stores/boards";
import { useConfigStore } from "@/stores/config";

const boardStore = useBoardStore();
const { boards } = storeToRefs(boardStore);

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);

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
