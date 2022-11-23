<script setup>
import {
  NA,
  NSpace,
  NForm,
  NFormItem,
  NInput,
  NH1,
  NH5,
  NButton,
  useMessage,
  NSelect,
} from "naive-ui";
import { useRouter } from "vue-router";
import { computed, ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { getCampusList } from "../api/campus";
import { createStudent } from "../api/user";

const router = useRouter();
// initialize auth store and can be shared by all components
const authStore = useAuthStore();
const message = useMessage();

const formRef = ref(null);
const registerModel = ref({
  username: "",
  password: "",
  campus: "",
  display_name: "",
  telephone: "",
  wx: "",
});

// formRules for validation
const formRules = {
  username: {
    required: true,
    min: 3,
    max: 20,
    message: "Username must be between 3 and 20 characters",
    trigger: "blur",
  },
  password: {
    required: true,
    min: 3,
    max: 20,
    message: "Password must be between 3 and 20 characters",
    trigger: "blur",
  },
  display_name: {
    required: true,
    min: 3,
    max: 20,
    message: "Display name must be between 3 and 20 characters",
    trigger: "blur",
  },
  telephone: {
    required: true,
    trigger: "blur",
  },
  wx: {
    required: false,
  },
  campus: {
    required: true,
    message: "Please select a campus",
    trigger: "blur",
  },
};

const campusList = ref([]);
onMounted(async () => {
  // getCampusList() comes from src\api\campus.js
  const response = await getCampusList();
  registerModel.value.campus = response[0].id;
  campusList.value = response.map((item) => ({
    label: item.name,
    value: item.id,
  }));
});

const loading = ref(false);
const disabled = computed(
  () =>
    registerModel.value.username === "" || registerModel.value.password === ""
);

// handle register function
const handleRegister = async () => {
  loading.value = true;
  try {
    // console.log(registerModel.value);

    await createStudent(registerModel.value)

    loading.value = false;
    message.success("Register successfully");
    router.push("/login");
  } catch (e) {
    message.error(e.response.data.message);
  }
};
</script>

<template>
  <div class="register">
    <n-space class="register-card" vertical>
      <n-h1>Create your KPI account</n-h1>
      <n-h5>Create your account to continue</n-h5>

      <!-- register form -->
      <!-- ref property in form for form checking -->
      <n-form ref="formRef" :model="registerModel" :rules="formRules">
        <n-form-item path="username" label="Username">
          <n-input
            type="text"
            placeholder="Please Input"
            v-model:value="registerModel.username"
          />
        </n-form-item>
        <n-form-item path="password" label="Password">
          <n-input
            type="password"
            placeholder="Please Input"
            v-model:value="registerModel.password"
          />
        </n-form-item>

        <!-- new adding -->
        <n-form-item path="campus" label="Campus">
          <n-select v-model:value="registerModel.campus" :options="campusList">
          </n-select>
        </n-form-item>
        <n-form-item path="display_name" label="Display Name">
          <n-input
            type="text"
            placeholder="Please Input"
            v-model:value="registerModel.display_name"
          />
        </n-form-item>
        <n-form-item path="telephone" label="Telephone Number">
          <n-input
            type="text"
            placeholder="Please Input"
            v-model:value="registerModel.telephone"
          />
        </n-form-item>
        <n-form-item path="wx" label="Wechat Number">
          <n-input
            type="text"
            placeholder="Please Input"
            v-model:value="registerModel.wx"
          />
        </n-form-item>

        <n-space justify="end">
          <n-button
            type="primary"
            tag="a"
            size="large"
            :loading="loading"
            :disabled="disabled"
            @click="handleRegister"
          >
            register
          </n-button>
        </n-space>
      </n-form>
    </n-space>
  </div>
</template>

<style lang="less" scoped>
.register {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: end;
  align-items: center;
}
.register-card {
  width: 400px;
  margin: 0 auto;
}
</style>
