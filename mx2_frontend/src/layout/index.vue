<script setup>
import LayoutContent from "./LayoutContent.vue";
import LayoutHeader from "./LayoutHeader.vue";
import LayoutSidebar from "./LayoutSidebar.vue";
import { NLayout } from "naive-ui";
</script>

<template>
  <n-layout position="absolute" has-sider>
    <layout-sidebar />
    <n-layout>
      <layout-header />
      <layout-content />
    </n-layout>
  </n-layout>
</template>
