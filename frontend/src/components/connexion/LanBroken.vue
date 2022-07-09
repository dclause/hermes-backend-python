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
            Oops ... the connection was lost
          </v-card-title>
          <v-card-subtitle>
            This is ground control to robot... please respond
            !
          </v-card-subtitle>
        </div>
      </div>
    </v-card>
  </v-layout>
</template>

<script lang="ts" setup>
import SvgRobotBroken from "@/components/icons/SvgRobotBroken.vue";
// prettier: no-newline
</script>
