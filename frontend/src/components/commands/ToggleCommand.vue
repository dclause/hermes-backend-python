<template>
  <v-switch
    v-model="value"
    :label="label"
    color="primary"
    hide-details
    inline
    inset
  />
</template>

<script lang="ts" setup>
import { defineModel } from "@/composables/vmodel";

const props = defineProps({
  modelValue: Boolean,
  label: String
});

const value = defineModel(props);
</script>
