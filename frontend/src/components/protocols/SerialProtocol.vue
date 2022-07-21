<template>
  Protocol: {{ protocol.name }} - {{ protocol.port }}
</template>

<script lang="ts" setup>

defineProps({
  protocol: {
    type: Object,
    required: true
  }
});

</script>