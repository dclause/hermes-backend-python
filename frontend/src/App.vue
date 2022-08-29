<!--
Main app component: defines a single layout for all pages.
-->

<template>
  <v-app id="hermes">
    <!-- Drawer: sidebar on the left-->
    <v-navigation-drawer
      app
      clipped
      mini-variant
      permanent
      rail
    >
      <v-tooltip>
        <template #activator="{ props }">
          <v-avatar
            class="d-block text-center mx-auto mt-4 pa-1"
            color=""
            size="60"
            v-bind="props"
          >
            <svg-robot title="test" />
          </v-avatar>
        </template>
        <span>{{ name }}</span>
      </v-tooltip>
      <v-divider class="mx-3 my-5" />

      <main-menu-list />
    </v-navigation-drawer>

    <!-- AppBar: top bar-->
    <v-app-bar
      app
      color="primary"
      density="compact"
    >
      <v-app-bar-title>HERMES - a Robot Management System</v-app-bar-title>

      <template #append>
        <LanControl />
        <v-btn icon="mdi-cog" />
      </template>
    </v-app-bar>

    <!-- Main: -->
    <v-main class="grey lighten-2">
      <v-container
        class="pa-8"
        fluid
        style="overflow-x:auto;"
      >
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import LanControl from "@/components/connexion/LanControl.vue";
import MainMenuList from "@/components/menus/MainMenuList.vue";
import SvgRobot from "@/components/icons/SvgRobot.vue";
import { storeToRefs } from "pinia";
import { useProfileStore } from "@/stores/profile";

const profileStore = useProfileStore();
const { name } = storeToRefs(profileStore);

</script>
