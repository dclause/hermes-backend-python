<template>
  <v-list nav>
    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          prepend-icon="mdi-memory"
          title="Boards"
          to="boards"
          v-bind="props"
        />
      </template>
      <span>Boards</span>
    </v-tooltip>

    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          prepend-icon="mdi-robot-industrial"
          title="Groups"
          to="devices"
          v-bind="props"
        />
      </template>
      <span>Groups</span>
    </v-tooltip>
  </v-list>
</template>