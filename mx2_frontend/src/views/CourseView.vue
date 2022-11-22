<script setup>
import { useRoute } from "vue-router";
import { ref, watchEffect } from "vue";
import { getCourse, getLectureList, createLecture } from "../api/course";
import {
  NSpace,
  NCard,
  NDivider,
  NH1,
  NH3,
  NP,
  NGrid,
  NGridItem,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NDatePicker,
  useMessage,
} from "naive-ui";
import CourseDetails from "../components/CourseDetails.vue";
import CourseLecture from "../components/CourseLecture.vue";

import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

const route = useRoute();
const message = useMessage();
const courseData = ref(null);
const lectureList = ref([]);
const showNewLecture = ref(false);

const newLectureForm = ref({
  title: "",
  streaming_url: "",
  recording_url: "",
  scheduled_time: new Date(),
});

const createNewLecture = async () => {
  try {
    await createLecture(
      courseData.value.id,
      newLectureForm.value.title,
      newLectureForm.value.streaming_url,
      newLectureForm.value.recording_url,
      newLectureForm.value.scheduled_time.toISOString().split(".")[0]
    );

    message.success("Lecture has been created.");
    lectureList.value = await getLectureList(route.params.id);

    showNewLecture.value = false;
    // setTimeout(() => {
    //   window.location.reload();
    // }, 1500);
  } catch (e) {
    console.log(e);
  }
};

const handleAddNew = () => {
  showNewLecture.value = true;
};

const isPurchased = ref(null);

watchEffect(async () => {
  if (route.params.id) {
    const course = await getCourse(route.params.id);
    courseData.value = course;
    document.title = course.name;
    lectureList.value = await getLectureList(route.params.id);
  }

  if (
    authStore.getUserInfo?.user_type === "User.Admin" ||
    authStore.getUserInfo?.enrolled_courses
      .map((c) => c.id)
      .includes(route.params.id)
  ) {
    isPurchased.value = true;
  } else {
    isPurchased.value = false;
  }
});
</script>

<template>
  <n-space vertical v-if="courseData">
    <n-h1
      >{{ courseData.name }}
      <span class="course-data"> ({{ courseData.uni_course_code }})</span>
    </n-h1>

    <course-details
      :course="courseData"
      :isPurchased="isPurchased"
    ></course-details>
    <n-divider></n-divider>

    <n-card v-if="isPurchased === false">
      <n-space vertical align="center">
        <n-h3> You haven't purchased this course</n-h3>
        <n-p> Please contact teachers or admins to order it</n-p>
      </n-space>
    </n-card>

    <div v-else>
      <n-grid :cols="3" x-gap="24" y-gap="12">
        <n-grid-item v-for="lecture in lectureList" :key="lecture.id">
          <course-lecture
            :lecture="lecture"
            :courseId="courseData.id"
          ></course-lecture>
        </n-grid-item>
      </n-grid>
      <n-divider>
        <n-button type="success" @click="handleAddNew">
          Add New Lecture
        </n-button>
      </n-divider>
    </div>
  </n-space>

  <!-- dialoag -->
  <n-modal v-model:show="showNewLecture">
    <n-card
      style="width: 400px; margin: 0 auto"
      title="Add new lecture"
      :bordered="false"
      size="huge"
      aria-modal="true"
    >
      <n-form
        ref="newLectureFormRef"
        :model="newLectureForm"
        label-placement="left"
        label-width="auto"
      >
        <n-form-item label="title" path="title">
          <n-input v-model:value="newLectureForm.title" placeholder="" />
        </n-form-item>
        <n-form-item label="Streaming Link" path="streaming_url">
          <n-input
            v-model:value="newLectureForm.streaming_url"
            placeholder=""
          />
        </n-form-item>
        <n-form-item label="Recording Link" path="recording_url">
          <n-input
            v-model:value="newLectureForm.recording_url"
            placeholder=""
          />
        </n-form-item>
        <n-form-item label="Datetime" path="scheduled_time">
          <n-date-picker
            v-model:value="newLectureForm.scheduled_time"
            placeholder=""
            type="datetime"
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space>
          <n-button type="primary" @click="createNewLecture">Create</n-button>
          <n-button @click="showNewLecture = false">Cancel</n-button>
        </n-space>
      </template>
    </n-card>
  </n-modal>
</template>

<style scoped>
.course-data {
  color: grey;
}
</style>
