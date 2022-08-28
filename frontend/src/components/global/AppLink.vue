<template>
  <router-link
    :to="to"
    class="app-link text-decoration-none text-primary font-weight-bold"
  >
    <slot />
  </router-link>
</template>

<script setup>

defineProps({
  to: {
    type: Object,
    required: true
  }
});
</script>