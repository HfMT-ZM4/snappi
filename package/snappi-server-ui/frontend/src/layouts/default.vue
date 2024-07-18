<template>
  <v-app>
    <SideBar />
    <v-main>
      <ActionBar />
      <ConfigCheck />
      <router-view />
    </v-main>
    <AppFooter />
  </v-app>
</template>
