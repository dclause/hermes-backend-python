<template>
  <router-view v-if="connected" />
  <lan-broken v-else />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useConfigStore } from "@/stores/config";
import LanBroken from "@/components/connexion/LanBroken.vue";

const configStore = useConfigStore();
const { connected } = storeToRefs(configStore);

</script>