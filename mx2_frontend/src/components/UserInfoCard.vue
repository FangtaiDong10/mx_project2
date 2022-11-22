<script setup>
import { defineProps, computed } from "vue";
import { NCard, NSpace, NH2, NP, NAvatar, NTag, NIcon } from "naive-ui";
import { Person } from "@vicons/ionicons5";
const props = defineProps(["userInfo"]);
const userType = computed(() => props.userInfo.user_type.split(".")[1]);
</script>

<template>
  <n-card
    :segmented="{
      content: true,
      footer: 'soft',
    }"
    v-if="props.userInfo"
  >
    <template #default>
      <n-space justify="space-between" align="center">
        <n-space vertical>
          <n-h2> Welcome {{ props.userInfo.display_name }}</n-h2>
          <n-p> User ID: {{ props.userInfo.id }}</n-p>
          <n-p> Current Campus: {{ props.userInfo.campus }}</n-p>
        </n-space>
        <n-avatar :size="96" round>
          <img src="~@/assets/david.png" alt="" />
        </n-avatar>
      </n-space>
    </template>
    <template #footer>
      <n-space>
        <n-tag type="success" round :bordered="false">
          {{ userType }}
          <template #icon>
            <n-icon :component="Person"></n-icon>
          </template>
        </n-tag>
        <n-tag
          v-for="permission in props.userInfo.permissions"
          :key="permission"
          round
          :bordered="false"
          >{{ permission }}</n-tag
        >
      </n-space>
    </template>
  </n-card>
</template>
