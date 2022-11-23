<script setup>
import { useAuthStore } from "../stores/auth";
import UserInfoCard from "../components/UserInfoCard.vue";
import CoursesStatus from "../components/CoursesStatus.vue";
import CourseList from "../components/CourseList.vue";
import { ref, onMounted } from "vue";

import { getCourseList } from "../api/course";

import { NGrid, NGridItem, NDivider } from "naive-ui";
const authStore = useAuthStore();
authStore.reload();

const enrolledCourses = ref({});

onMounted(async () => {
  const response = await getCourseList();

  response.items = response.items.filter((course) =>
    authStore.getUserInfo?.enrolled_courses?.map((c) => c.id).includes(course.id)
  );

  enrolledCourses.value = response;
});
</script>
<template>
  <n-grid
    cols="1 m:2"
    :x-gap="12"
    :y-gap="8"
    responsive="screen"
    v-if="authStore.getUserInfo"
  >
    <n-grid-item>
      <user-info-card :user-info="authStore.getUserInfo"></user-info-card>
    </n-grid-item>

    <n-grid-item>
      <courses-status :user-info="authStore.getUserInfo" />
    </n-grid-item>
  </n-grid>

  <n-divider />

  <course-list :courseData="enrolledCourses"></course-list>

  <!-- no need parentheses(braket) when using pinia getters -->
  <!-- {{ authStore.getUserInfo? }} -->
</template>
