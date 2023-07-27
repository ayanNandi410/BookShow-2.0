<script setup>
import { RouterView } from "vue-router";
import Navbar from "./components/navbar.vue";
import PageFooter from "./components/pageFooter.vue";
</script>

<template>
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Book Show</title>
    </head>
    <body>
      <Navbar />
      <RouterView />
      <PageFooter />
    </body>
  </html>
</template>

<style>
.body {
  margin: 8% auto;
}
</style>
