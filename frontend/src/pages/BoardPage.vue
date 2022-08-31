<template>
  <div class="d-flex justify-space-between align-center">
    <h1 class="text-h5 text-md-h4">
      {{ board.name }}
    </h1>
    <v-btn
      icon="mdi-dots-vertical"
      variant="plain"
    />
  </div>
  <div class="ml-2 text-overline">
    {{ getController }} {{ board.model }}
  </div>

  <v-tabs
    v-model="tab"
    background-color="transparent"
    color="black"
    slider-color="primary"
  >
    <v-tab value="info">
      {{ $t("pages.board.tab.info") }}
    </v-tab>
    <v-tab value="controls">
      {{ $t("components.board.controls") }}
    </v-tab>
    <v-tab value="inputs">
      {{ $t("components.board.inputs") }}
    </v-tab>
    <v-tab value="history">
      {{ $t("pages.board.tab.history") }}
    </v-tab>
  </v-tabs>

  <v-window
    v-model="tab"
  >
    <v-window-item
      :reverse-transition="false"
      :transition="false"
      value="info"
    >
      <v-card>
        <v-card-text>
          <div>{{ $t("components.board.type") }}: {{ getController }} {{ board.model }}</div>
          <div>
            {{ $t("components.board.status") }}:
            {{ board.connected ? $t("global.connexion.status.connected") : $t("global.connexion.status.offline") }}
          </div>
          <div>
            {{ $t("components.board.protocol") }}:
            <component
              :is="useProtocol(board.protocol.controller)"
              :protocol="board.protocol"
            />
          </div>
        </v-card-text>
      </v-card>
    </v-window-item>

    <v-window-item
      :reverse-transition="false"
      :transition="false"
      value="controls"
    >
      <v-card>
        <v-card-text v-if="Object.keys(board.actions).length">
          <div
            v-for="(device, key) in board.actions"
            :key="key"
          >
            <component
              :is="useDevice(device.controller)"
              v-model="board.actions[key]"
              :board="board"
              class="md-2"
              info=""
              variant="compact"
            />
            <v-divider />
          </div>
        </v-card-text>
        <v-card-text v-else>
          <em>{{ $t("components.board.no_actions") }}</em>
        </v-card-text>
      </v-card>
    </v-window-item>

    <v-window-item
      :reverse-transition="false"
      :transition="false"
      value="inputs"
    >
      <v-card>
        <v-card-text v-if="Object.keys(board.inputs).length">
          <div
            v-for="(device, key) in board.inputs"
            :key="key"
          >
            <component
              :is="useDevice(device.controller)"
              v-model="board.inputs[key]"
              :board="board"
              class="md-2"
              info=""
              variant="compact"
            />
            <v-divider />
          </div>
        </v-card-text>
        <v-card-text v-else>
          <em>{{ $t("components.board.no_inputs") }}</em>
        </v-card-text>
      </v-card>
    </v-window-item>
    <v-window-item
      :reverse-transition="false"
      :transition="false"
      value="history"
    >
      <v-card>
        <v-card-text>
          @todo
        </v-card-text>
      </v-card>
    </v-window-item>
  </v-window>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useBoardStore } from "@/stores/boards";
import { useBoardController } from "@/composables/boards";
import { useDevice } from "@/composables/devices";
import { useProtocol } from "@/composables/protocols";

const route = useRoute();
const boardId: number = Number.parseInt(route.params.boardId as string);

const boardStore = useBoardStore();
const board = boardStore.getBoard(boardId);
const getController = useBoardController(board.controller as string);

const tab = ref("controls");
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
