<script setup>
import { defineProps, computed } from "vue";
import { NGrid, NGridItem, NCard, NA } from "naive-ui";
import { useAuthStore } from "../stores/auth";
const props = defineProps(["courseData"]);
const courseList = computed(() => props.courseData.items);

const authStore = useAuthStore();

const isPurchasedCourse = (course_id) => {
  if (authStore.getUserInfo?.user_type == "User.Admin") {
    return true;
  } else {
    return authStore.getUserInfo?.enrolled_courses
      .map((c) => c.id)
      .includes(course_id);
  }
};
</script>

<template>
  <n-grid :cols="4" :x-gap="12" :y-gap="8">
    <n-grid-item v-for="course in courseList" :key="course.id">
      <n-card :title="course.name" class="course-card">
        <template #cover>
          <n-a
            :href="`/${isPurchasedCourse(course.id) ? 'courses' : 'browse'}/${
              course.id
            }`"
          >
            <img :src="course.cover_image" alt="" style="height: 100%" />
          </n-a>
        </template>
        <template #footer> A${{ course.original_price }}K </template>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>

<style lang="less" scoped>
.course-card {
  :deep(.n-card-header) {
    padding-bottom: 8px;
  }

  :deep(.n-card__footer) {
    margin-left: auto;
    padding-bottom: 8px;
    color: orange;
  }
}
</style>
