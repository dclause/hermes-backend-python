<!--
Main app component: defines a single layout for all pages.
-->

<template>
  <v-app id="hermes">
    <!-- Drawer: sidebar on the left-->
    <v-navigation-drawer app clipped mini-variant permanent rail>
      <v-avatar
        class="d-block text-center mx-auto mt-4 pa-1"
        color=""
        size="45"
      >
        <svg-robot />
      </v-avatar>
      <v-divider class="mx-3 my-5"></v-divider>

      <main-menu-list />
    </v-navigation-drawer>

    <!-- AppBar: top bar-->
    <v-app-bar app color="primary" density="compact">
      <v-app-bar-title>HERMES - a Robot Management System</v-app-bar-title>

      <template v-slot:append>
        <LanControl />
        <v-btn icon="mdi-cog"></v-btn>
      </template>
    </v-app-bar>

    <!-- Main: -->
    <v-main class="grey lighten-2">
      <v-container class="pa-8" fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import LanControl from "@/components/connexion/LanControl.vue";
import MainMenuList from "@/components/menus/MainMenuList.vue";
import SvgRobot from "@/components/icons/SvgRobot.vue";</script>
