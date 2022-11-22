<script setup>
import { RouterView } from "vue-router";
import { NLayoutContent } from "naive-ui";
</script>

<template>
  <n-layout-content content-style="padding: 24px">
    <router-view></router-view>
  </n-layout-content>
</template>
