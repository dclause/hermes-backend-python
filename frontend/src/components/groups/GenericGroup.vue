<template>
  <v-card
    :title="group.name"
    variant="flat"
  >
    <v-card-text
      v-if="children.length"
      :class="groupClasses"
      class="group pl-4"
    >
      <div
        v-for="child in children"
        :key="child.id"
        class="group-inner"
      >
        <component
          :is="useDevice(boards[child.board].actions[child.device].controller)"
          v-if="child.type === 'device'"
          v-model="boards[child.board].actions[child.device]"
          :board="boards[child.board]"
          class="md-2"
          info=""
          variant="compact"
        />
        <generic-group
          v-else
          :group="child"
        />
      </div>
    </v-card-text>
    <v-card-text
      v-else
      class="pl-4"
    >
      <em>{{ $t("components.group.no_content") }}</em>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>

import { useGroupStore } from "@/stores/groups";
import { storeToRefs } from "pinia";
import { useBoardStore } from "@/stores/boards";
import { useDevice } from "@/composables/devices";
import { computed } from "vue";
import type { GroupConfigurationProperties, GroupDeviceConfigurationProperties } from "@/composables/groups";

const props = defineProps({
  group: {
    type: Object,
    required: true
  }
});

// Boards
const boardStore = useBoardStore();
const { boards } = storeToRefs(boardStore);

// Groups
const groupStore = useGroupStore();
const { groups } = storeToRefs(groupStore);

const children = computed(() => {
  const childGroups: [] = groups.value.filter(group => group.parent === props.group.id) as [];
  const devices: [] = props.group.content;
  return childGroups
    .concat(devices)
    .map((child: GroupConfigurationProperties | GroupDeviceConfigurationProperties) => {
      return { ...child, type: ("parent" in child) ? "group" : "device" };
    })
    .sort((a: GroupConfigurationProperties | GroupDeviceConfigurationProperties, b: GroupConfigurationProperties | GroupDeviceConfigurationProperties) => a.order - b.order);
});

const groupClasses = computed(() => {
  switch (props.group.layout) {
    case undefined:
    case "100":
      return "layout-100 d-flex flex-column";
    case "50_50":
      return "layout-50_50 d-flex flex-row flex-grow-1";
  }
  return "";
});

</script>

<style lang="scss">
.group {
  flex: 0 0 auto;

  &-inner {
    min-width: 0;
    flex: 1;
    margin: 0;
    border: 1px solid;
    border-color: rgba(var(--v-border-color), var(--v-border-opacity));
    overflow: hidden;
  }

  &.layout {
    &-100 > .group-inner {
      border-width: 0 0 1px 0;

      &:first-of-type {
        border-top-width: 0;
      }

      &:last-of-type {
        border-bottom-width: 0;
      }
    }

    &-50_50 > .group-inner {
      border-width: 0 1px 0 1px;

      &:first-of-type {
        border-left-width: 0;
      }

      &:last-of-type {
        border-right-width: 0;
      }
    }
  }
}
</style>