<script setup>
import CourseList from "../components/CourseList.vue";
import { getCourseList } from "../api/course";
import { ref, onMounted } from "vue";

const courseResponse = ref({});

onMounted(async () => {
  const data = await getCourseList();
  courseResponse.value = data;
});
</script>

<template>
  <course-list :courseData="courseResponse"></course-list>
</template>
