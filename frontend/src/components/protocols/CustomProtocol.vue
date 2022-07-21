<template>
  Protocol: {{ protocol.name }}
</template>

<script lang="ts" setup>

defineProps({
  protocol: {
    type: Object,
    required: true
  }
});

</script>