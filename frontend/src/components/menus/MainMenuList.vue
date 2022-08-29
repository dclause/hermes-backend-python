<template>
  <v-list
    class="text-center"
    nav
  >
    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          :active="isRouteActive('boards') || isRouteActive('board')"
          :to="{ name: 'boards' }"
          style="font-size: 1.2em;"
          v-bind="props"
        >
          <v-icon
            icon="mdi-memory"
            width="40"
          />
        </v-list-item>
      </template>
      <span>{{ $t("pages.boards.menu") }}</span>
    </v-tooltip>

    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          :active="isRouteActive('groups')"
          :to="{ name: 'devices'}"
          v-bind="props"
        >
          <v-icon
            icon="mdi-robot-industrial"
            width="40"
          />
        </v-list-item>
      </template>
      <span>{{ $t("pages.groups.menu") }}</span>
    </v-tooltip>
  </v-list>
</template>

<script setup>

import { useRoute } from "vue-router";

const route = useRoute();
const isRouteActive = (name) => {
  return route.name === name;
};

</script>