<template>
  <v-layout class="align-center h-100">
    <v-card class="d-print-inline-block mx-auto pa-5">
      <div class="align-center d-flex flex-no-wrap">
        <v-avatar
          class="pa-2"
          rounded="0"
          size="125"
        >
          <svg-robot-broken />
        </v-avatar>
        <div>
          <v-card-title class="text-h5">
            {{ $t("pages.notfound.title") }}
          </v-card-title>
          <v-card-subtitle>
            {{ $t("pages.notfound.description") }}
            <app-link :to="{name: 'home'}">
              {{ $t("pages.notfound.link") }}
            </app-link>
            !
          </v-card-subtitle>
        </div>
      </div>
    </v-card>
  </v-layout>
</template>

<script lang="ts" setup>

import AppLink from "@/components/global/AppLink.vue";
import SvgRobotBroken from "@/components/icons/SvgRobotBroken.vue";</script>