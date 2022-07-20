<template>
  <v-list nav>
    <v-tooltip>
      <template #activator="{ props }">
        <v-list-item
          prepend-icon="mdi-robot"
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
          link
          prepend-icon="mdi-robot-industrial"
          title="Devices"
          to="devices"
          v-bind="props"
        />
      </template>
      <span>Devices</span>
    </v-tooltip>
  </v-list>
</template>