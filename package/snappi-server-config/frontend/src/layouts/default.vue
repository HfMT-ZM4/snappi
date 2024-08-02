<template>
  <v-app>
    <SideBar />
    <v-main>
      <ActionBar />
      <ConfigCheck />
      <RestartPrompt />
      <router-view />
    </v-main>
    <AppFooter />
  </v-app>
</template>
