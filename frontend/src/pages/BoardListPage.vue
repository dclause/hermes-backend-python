<template>
  <component :is="useBoard(board.type)" v-for="(board, id) in boards" :key="board.id" v-model="boards[id]" />
  <lan-broken v-if="!hasBoards" />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useBoard } from "@/composables/boards";
import { useBoardStore } from "@/stores/boards";
import LanBroken from "@/components/connexion/LanBroken.vue";

const boardStore = useBoardStore();
const { boards } = storeToRefs(boardStore);
const hasBoards = Object.keys(boards).length;

</script>
