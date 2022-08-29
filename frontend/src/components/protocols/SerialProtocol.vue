<template>
  {{ prefix }} <span class="d-none d-md-inline-block">
    {{ $t("components.protocol.serial") }}
  </span>&nbsp;{{ protocol.port }}
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