<template>
  <div class="d-flex justify-space-between align-center mb-4">
    <h1 class="text-h5 text-md-h4">
      {{ $t("pages.groups.title") }}
    </h1>
    <v-btn
      :icon="$vuetify.display.xs === true"
      color="primary"
      @click=""
    >
      <v-icon>
        mdi-plus
      </v-icon>
      <span class="d-none d-sm-block">{{ $t("components.group.new") }}</span>
    </v-btn>
  </div>

  <generic-group
    v-for="group in childGroupsOf(0)"
    :key="group.id"
    :group="group"
  />
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useGroupStore } from "@/stores/groups";
import GenericGroup from "@/components/groups/GenericGroup.vue";

// Groups
const groupStore = useGroupStore();
const { groups } = storeToRefs(groupStore);

const childGroupsOf = (parent: number) => groups.value.filter(group => group.parent === parent);
</script>
