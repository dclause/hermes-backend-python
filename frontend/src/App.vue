<!--
Main app component: defines a single layout for all pages.
-->

<template>
  <v-app id="hermes">
    <!-- Drawer: sidebar on the left-->
    <v-navigation-drawer
      :rail="drawer"
      app
      clipped
      mini-variant
      @click.capture="this.drawer = !this.drawer"
    >
      <v-avatar
        class="d-block text-center mx-auto mt-4"
        color="grey darken-1"
        size="36"
      ></v-avatar>
      <v-divider class="mx-3 my-5"></v-divider>
    </v-navigation-drawer>

    <!-- AppBar: top bar-->
    <v-app-bar app color="primary" density="compact">
      <v-app-bar-title>HERMES</v-app-bar-title>

      <template v-slot:append>
        <LanControl />
        <v-btn icon="mdi-cog"></v-btn>
      </template>
    </v-app-bar>

    <!-- Main: -->
    <v-main class="grey lighten-2">
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import LanControl from "@/components/LanControl.vue";

const drawer = ref(true);
</script>
