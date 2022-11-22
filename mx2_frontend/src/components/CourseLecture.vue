<script setup>
import { ref, defineProps, computed } from "vue";
import {
  NCard,
  NThing,
  NAvatar,
  NSpace,
  NTag,
  NIcon,
  NDescriptions,
  NDescriptionsItem,
  NDivider,
  NA,
  NModal,
  NUpload,
  NUploadDragger,
  useMessage,
} from "naive-ui";
import {
  Videocam,
  DocumentAttach,
  CloudUpload,
  Archive,
} from "@vicons/ionicons5";
import { uploadAttachment } from "../api/course";

const props = defineProps(["lecture", "courseId"]);

const scheduled_time = computed(
  () => new Date(props.lecture.scheduled_time + "Z")
);

const showUpload = ref(false);
// const handleAddNewAttachment = () => {};

const message = useMessage();

// upload file handler
const uploadRequest = async ({ file, onFinish, onError, onProgress }) => {
  // console.log(file);
  try {
    await uploadAttachment(
      props.courseId,
      props.lecture.id,
      file.file,
      file.name,
      "attachment",
      ({ percent }) => {
        onProgress({ percent: Math.ceil(percent) });
      }
    );
    message.success("File Uploaded. Page will be reload within 1.5 seconds");
    setTimeout(() => {
      window.location.reload();
    }, 1500);
    onFinish();
  } catch (e) {
    onError();
  }
};
</script>
<template>
  <n-card>
    <n-thing>
      <template #avatar>
        <n-avatar>
          <n-icon :component="Videocam" />
        </n-avatar>
      </template>

      <template #header-extra> {{ props.lecture.title }}</template>

      <template #description>
        <span class="lecture-id">
          {{ props.lecture.id }}
        </span>
      </template>

      <!-- main content -->

      <n-descriptions label-placement="left" :column="1">
        <n-descriptions-item label="Time">
          {{ scheduled_time.toLocaleString() }}
        </n-descriptions-item>
        <n-descriptions-item label="Streaming">
          <n-a :href="props.lecture.streaming_url">Jump to Zoom</n-a>
        </n-descriptions-item>
        <n-descriptions-item label="Recording">
          <n-a :href="props.lecture.recording_url">Jump to Zoom</n-a>
        </n-descriptions-item>
      </n-descriptions>

      <template #footer>
        <n-divider class="attachment-divider">Attachments</n-divider>
        <n-space>
          <n-tag
            v-for="attachment in props.lecture.attachments"
            :key="attachment.name"
            round
            :bordered="false"
            size="small"
            type="success"
          >
            <template #icon>
              <n-icon :component="DocumentAttach"></n-icon>
            </template>
            <n-a :href="attachment.signed_url"> {{ attachment.name }} </n-a>
          </n-tag>
          <n-tag round :bordered="false" size="small" type="success">
            <template #icon>
              <n-icon :component="CloudUpload"></n-icon>
            </template>
            <n-a @click="showUpload = true"> Upload +</n-a>
          </n-tag>
        </n-space>
      </template>
    </n-thing>
  </n-card>

  <n-modal v-model:show="showUpload">
    <n-card
      style="width: 400px"
      title="Upload new attachment"
      :bordered="false"
      size="huge"
    >
      <n-upload directory-dnd="false" :custom-request="uploadRequest">
        <n-upload-dragger>
          <div style="margin-bottom: 12px">
            <n-icon size="48" :depth="3" :component="Archive"></n-icon>
          </div>
          Click or drag file to this area to upload
        </n-upload-dragger></n-upload
      >
    </n-card>
  </n-modal>
</template>

<style scoped>
.lecture-id {
  font-size: 12px;
  color: gray;
}

.attachment-divider {
  font-size: 12px;
  color: gray;
}
</style>
