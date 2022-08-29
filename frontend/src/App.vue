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
      <v-app-bar-title>HERMES - {{ $t("global.app.slogan") }}</v-app-bar-title>

      <template #append>
        <lan-control />
        <v-btn
          :to="{name:'settings'}"
          icon="mdi-cog"
        />
      </template>
    </v-app-bar>

    <!-- Main: -->
    <v-main class="grey lighten-2">
      <v-container
        class="pa-8"
        fluid
        style="overflow-x:auto;"
      >
        <component :is="layout">
          <router-view />
        </component>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useProfileStore } from "@/stores/profile";
import LanControl from "@/components/connexion/LanControl.vue";
import MainMenuList from "@/components/menus/MainMenuList.vue";
import SvgRobot from "@/components/icons/SvgRobot.vue";

const profileStore = useProfileStore();
const { name } = storeToRefs(profileStore);
const route = useRoute();

const layout = ref("ConnectedLayout");
watch(() => route.meta, (meta) => {
  layout.value = meta.layout as string || "ConnectedLayout";
});
</script>
