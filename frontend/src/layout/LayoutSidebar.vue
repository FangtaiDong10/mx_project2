<script setup>
import { NLayoutSider, NA, NMenu, NIcon } from "naive-ui";
import { ref, h, watchEffect } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { Home, Book, Grid, Cart } from "@vicons/ionicons5";
import { useAuthStore } from "../stores/auth";
import { storeToRefs } from "pinia";

// convert authStore to reference
const authStore = useAuthStore();
const auth = storeToRefs(authStore);

const route = useRoute();
const collapsed = ref(false);
const currentKey = ref(null);

watchEffect(() => {
  // console.log(route.fullPath);
  if (route.fullPath.split("/").includes("browse")) {
    currentKey.value = "browse";
  } else {
    currentKey.value = route.fullPath.slice(1);
  }
});

// menu items
const createMenu = (coursesMenu) => {
  return [
    {
      label: "Home",
      key: "home",
      path: "/",
      icon: Home,
    },
    {
      label: "Orders",
      key: "orders",
      icon: Cart,
      path: "/orders",
    },
    {
      label: "All Forklifts",
      key: "browse",
      icon: Grid,
      path: "/browse",
    },
    {
      label: "My Forklifts",
      key: "courses",
      path: "/courses",
      icon: Book,
      children: coursesMenu,
    },
  ];
};

const menu = ref(createMenu([]));

watchEffect(() => {
  // menu.value = createMenu()

  // console.log(auth.userInfo);

  if (auth.userInfo.value?.enrolled_courses) {
    menu.value = createMenu(
      auth.userInfo.value.enrolled_courses.map((item) => ({
        label: item.name,
        key: "courses/" + item.id,
        path: "/courses/" + item.id,
      }))
    );
  }
});

const renderMenu = (menu) =>
  menu.map((item) => ({
    label: () =>
      item.children ? item.label : h(RouterLink, { to: item.path }, item.label),
    key: item.key,
    icon:
      item.icon != null
        ? () => h(NIcon, null, { default: () => h(item.icon) })
        : undefined,
    children: item.children ? renderMenu(item.children) : undefined,
  }));

const menuOptions = renderMenu(menu.value);
</script>

<template>
  <n-layout-sider
    bordered
    :width="240"
    show-trigger
    collapse-mode="width"
    v-model:collapsed="collapsed"
    :native-scrollbar="false"
  >
    <router-link to="/" custom v-slot="{ navigate, href }">
      <n-a class="logo" :href="href" @click="navigate">
        <img src="@/assets/kpi_logo1.jpg" alt="" />
        <span>KPI System</span>
      </n-a>
    </router-link>
    <n-menu
      v-model:value="currentKey"
      :options="menuOptions"
      :collapsed="collapsed"
    />
  </n-layout-sider>
</template>

<style lang="less" scoped>
.logo {
  position: sticky;
  top: 0;
  display: flex;
  padding: 20px;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 300;
  text-decoration: none;
  transition: padding 0.3s, font-size 0.3s;

  img {
    height: 32px;
    margin-right: 8px;
    transition: height 0.3s;
  }
}

.n-layout-sider--collapsed .logo {
  font-size: 0;
  padding: 12px;
  img {
    height: 22px;
    margin: auto;
  }
}
</style>
