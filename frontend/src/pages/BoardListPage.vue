<template>
  <v-container v-if="connected">
    <component
      :is="useBoard(board.controller)"
      v-for="board in boards"
      :key="board.id"
      :board-id="board.id"
    />
  </v-container>
  <lan-broken v-else />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useBoard } from "@/composables/boards";
import { useBoardStore } from "@/stores/boards";
import LanBroken from "@/components/connexion/LanBroken.vue";
import { useConfigStore } from "@/stores/config";

const boardStore = useBoardStore();
const { boards } = storeToRefs(boardStore);

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);
</script>
