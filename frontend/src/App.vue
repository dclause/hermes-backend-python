<template>
  <v-app id="hermes">
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

      <!--      <v-list class="pl-14" shaped>-->
      <!--        <v-list-item v-for="n in 5" :key="n" link>-->
      <!--          <v-list-item-title>Item {{ n }}</v-list-item-title>-->
      <!--        </v-list-item>-->
      <!--      </v-list>-->
    </v-navigation-drawer>

    <v-app-bar app color="primary" density="compact">
      <v-app-bar-title>HERMES</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-lan-check"></v-btn>
        <!-- lan-pending-->
        <v-btn icon="mdi-cog"></v-btn>
      </template>
    </v-app-bar>

    <v-main class="grey lighten-2">
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app> Tesst</v-footer>
  </v-app>
</template>

<script lang="ts" setup>
import { ref } from "vue";

const drawer = ref(true);
</script>
