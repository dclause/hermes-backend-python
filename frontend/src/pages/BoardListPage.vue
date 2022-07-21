<template>
  <v-container
    v-if="connected"
    class="d-flex align-content-start flex-wrap"
    fluid
  >
    <v-row no-gutters>
      <v-col
        v-for="board in boards"
        :key="board.id"
        cols="12"
        lg="6"
        xl="6"
      >
        <component
          :is="useBoard(board.controller)"
          :key="board.id"
          class="ma-2"
          :board-id="board.id"
        />
      </v-col>
    </v-row>
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
