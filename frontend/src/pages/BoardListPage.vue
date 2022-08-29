<template>
  <div class="d-flex justify-space-between align-center mb-4">
    <h1 class="text-h5 text-md-h4">
      My boards
    </h1>
    <v-btn
      :icon="$vuetify.display.xs === true"
      color="primary"
      @click=""
    >
      <v-icon>
        mdi-plus
      </v-icon>
      <span class="d-none d-sm-block">{{ $t("components.board.new") }}</span>
    </v-btn>
  </div>
  <v-table
    class="board-list"
    fixed-header
  >
    <thead>
      <tr>
        <th class="col-status d-none d-sm-table-cell">
          {{ $t("components.board.status") }}
        </th>
        <th class="col-name">
          {{ $t("components.board.name") }}
        </th>
        <th class="col-type d-none d-md-table-cell">
          {{ $t("components.board.type") }}
        </th>
        <th class="col-protocol d-none d-sm-table-cell">
          {{ $t("components.board.protocol") }}
        </th>

        <th class="col-actions text-center">
          {{ $t("components.board.actions") }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="board in boards"
        :key="board.id"
      >
        <td class="col-status d-none d-sm-table-cell">
          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-icon
                :icon="connected ? 'mdi-check-circle-outline' : 'mdi-close-circle'"
                v-bind="props"
              />
            </template>
            <span>
              {{ connected ? $t("global.connexion.status.connected") : $t("global.connexion.status.offline") }}
            </span>
          </v-tooltip>
        </td>
        <td class="col-name">
          <app-link :to="{ name: 'board', params: { boardId: board.id }}">
            {{ board.name }}
          </app-link>
        </td>
        <td class="col-type d-none d-md-table-cell">
          {{ getController(board) }} {{ board.model }}
        </td>
        <td class="col-protocol d-none d-sm-table-cell">
          <component
            :is="useProtocol(board.protocol.controller)"
            :protocol="board.protocol"
          />
        </td>

        <td class="col-actions text-center">
          <v-btn
            icon="mdi-pencil"
            size="x-small"
            variant="plain"
          />
          <v-btn
            icon="mdi-trash-can"
            size="x-small"
            variant="plain"
          />
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script lang="ts" setup>
import type { BoardConfigurationProperties } from "@/composables/boards";
import { useBoardController } from "@/composables/boards";
import { storeToRefs } from "pinia";
import { useBoardStore } from "@/stores/boards";
import { useConfigStore } from "@/stores/config";
import { useProtocol } from "@/composables/protocols";
import AppLink from "@/components/global/AppLink.vue";

const boardStore = useBoardStore();
const { boards } = storeToRefs(boardStore);

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);

const getController = (board: BoardConfigurationProperties) => useBoardController(board.controller as string);
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
