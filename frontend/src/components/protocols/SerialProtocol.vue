<template>
  {{ prefix }} <span class="d-none d-md-inline-block">Serial on&nbsp;</span>{{ protocol.port }}
</template>

<script lang="ts" setup>

defineProps({
  protocol: {
    type: Object,
    required: true
  },
  prefix: {
    type: String,
    default: ""
  }
});

</script>