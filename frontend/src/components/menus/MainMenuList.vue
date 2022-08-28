<template>
  <v-list nav>
    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          :to="{ name: 'boards'}"
          prepend-icon="mdi-memory"
          title="Boards"
          v-bind="props"
        />
      </template>
      <span>Boards</span>
    </v-tooltip>

    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          :to="{ name: 'devices'}"
          prepend-icon="mdi-robot-industrial"
          title="Groups"
          v-bind="props"
        />
      </template>
      <span>Groups</span>
    </v-tooltip>
  </v-list>
</template>