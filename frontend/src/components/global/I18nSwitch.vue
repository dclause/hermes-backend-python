<template>
  <div class="locale-changer">
    <v-select
      v-model="$i18n.locale"
      :hint="$t('page.settings.language.description')"
      :items="langs"
      :label="$t('page.settings.language.label')"
      item-title="name"
      item-value="code"
      persistent-hint
      variant="underlined"
    />
  </div>
</template>

<script setup>
const langs = [
  { code: "en", "name": "English" },
  { code: "fr", "name": "Français" }
];
</script>