<script setup>
import {
  NLayoutHeader,
  NBreadcrumb,
  NBreadcrumbItem,
  NSpace,
  NAvatar,
  NDropdown,
} from "naive-ui";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const auth = storeToRefs(authStore);

const router = useRouter();

const options = [{ label: "Sign Out", key: "logout" }];
const handleOptionSelect = async (key) => {
  // alert(key);
  if (key === "logout") {
    await authStore.logout();
    await router.push("/login");
  }
};
</script>
<template>
  <n-layout-header bordered>
    <n-breadcrumb>
      <n-breadcrumb-item>Dashboard</n-breadcrumb-item>
      <n-breadcrumb-item>Home</n-breadcrumb-item>
    </n-breadcrumb>

    <n-space align="center" class="navs" :size="20">
      <span>Hello {{ auth.userInfo?.value?.username }} !</span>
      <n-dropdown
        placement="bottom-end"
        :options="options"
        @select="handleOptionSelect"
      >
        <n-avatar size="small" round>
          <img src="@/assets/david.png" alt="" />
        </n-avatar>
      </n-dropdown>
    </n-space>
  </n-layout-header>
</template>

<style scoped>
.n-layout-header {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  padding: 8px 18px;
}

.navs {
  margin-left: auto;
  line-height: 1px;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>
