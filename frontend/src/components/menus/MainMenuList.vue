<template>
  <v-list nav>
    <v-tooltip>
      <template v-slot:activator="{ props }">
        <v-list-item prepend-icon="mdi-chip" title="Boards" to="boards" v-bind="props" />
      </template>
      <span>Boards</span>
    </v-tooltip>

    <v-tooltip>
      <template v-slot:activator="{ props }">
        <v-list-item link prepend-icon="mdi-connection" title="Devices" to="devices" v-bind="props" />
      </template>
      <span>Devices</span>
    </v-tooltip>
  </v-list>
</template>