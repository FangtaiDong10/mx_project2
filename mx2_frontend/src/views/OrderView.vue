<script setup>
import { ref, onMounted, h, reactive } from "vue";
import { getOrders } from "../api/order";
import { useAuthStore } from "../stores/auth";
import {
  NDataTable,
  NButton,
  NModal,
  NSpace,
  NH1,
  NDescriptions,
  NDescriptionsItem,
  NCard,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  useMessage,
} from "naive-ui";
import { payOrder } from "../api/order";
const authStore = useAuthStore();
const orderList = ref([]);
const loading = ref(true);
const showView = ref(false);

const showConfirmPayment = ref(false);
const paymentForm = ref({
  price: 0,
  comment: "",
});
const paymentFormRef = ref(null);
const selectedRow = ref(null);
const message = useMessage();

const paymentcolumn = reactive({
  key: "payment_status",
  title: "Payment Status",
  filter: true,
  filterMultiple: false,
  filterOptionValue: null,
  filterOptions: [
    {
      label: "Paid",
      value: true,
    },
    {
      label: "Unpaid",
      value: false,
    },
  ],
});

// columns for data table
const columns = ref([
  {
    key: "id",
    title: "Order ID",
  },
  {
    key: "course_name",
    title: "Course",
  },
  {
    key: "student_username",
    title: "Stundet",
  },
  {
    key: "campus",
    title: "Campus",
  },
  {
    key: "created_time",
    title: "Order Time",
  },
  {
    key: "original_price",
    title: "Price",
  },
  paymentcolumn,
  {
    key: "action",
    title: "Action",
    render(row) {
      return [
        h(
          NButton,
          {
            type: "primary",
            size: "small",
            onClick() {
              // console.log(row);
              showView.value = true;
              selectedRow.value = row;
            },
          },
          "View"
        ),

        // the second rendered component
        !row.data.paid &&
          // authStore.getUserInfo?.user_type == "User.Admin" &&
          h(
            NButton,
            {
              type: "primary",
              size: "small",
              style: {
                marginLeft: "8px",
              },

              onClick: () => {
                showConfirmPayment.value = true;
                // paymentForm change to reactive
                paymentForm.value = {
                  price: row.data.original_price,
                  comment: "",
                };
                selectedRow.value = row;
              },
            },
            "Pay"
          ),
      ];
    },
  },
]);

const pagination = reactive({
  // current page
  page: 1,

  // total number of pages
  pageCount: 1,
  pageSize: 10,
  prefix({ itemCount }) {
    return `${itemCount} orders in total`;
  },
});

// transfer data from api to data table format
const mapOrder = (order) => {
  return {
    id: order.id,
    course_name: order.course.name,
    student_username: order.student.username,

    // toLocalString() is used to convert the time to local time (in this case, Melbourne time (browser dependent))
    created_time: new Date(order.created_time + "Z").toLocaleString(),

    campus: order.campus.name,
    payment_status: order.paid ? "Paid" : "Not paid",
    original_price: "$" + order.original_price,

    // if we want to handle later, we need original data
    data: order,
  };
};

const handlePageChange = async (page) => {
  loading.value = true;

  const data = await getOrders(page, paymentcolumn.filterOptionValue);
  orderList.value = data.items.map(mapOrder);

  // pagination
  pagination.pageCount = data.total_pages;
  pagination.itemCount = data.counts;
  pagination.page = data.page_num;

  loading.value = false;
};

const handleFilterChange = async (filters) => {
  loading.value = true;

  const data = await getOrders(1, filters.payment_status);
  orderList.value = data.items.map(mapOrder);

  // pagination
  pagination.pageCount = data.total_pages;
  pagination.itemCount = data.counts;
  pagination.page = data.page_num;
  paymentcolumn.filterOptionValue = filters.payment_status;
  loading.value = false;
};

// fetch orders from backend and set to orderList.value
onMounted(async () => {
  const data = await getOrders();
  orderList.value = data.items.map(mapOrder);

  // pagination
  pagination.pageCount = data.total_pages;
  pagination.itemCount = data.counts;

  loading.value = false;
});

const confirmPayment = async () => {
  try {
    await payOrder(
      selectedRow.value.id,
      paymentForm.value.price,
      paymentForm.value.comment
    );
    showConfirmPayment.value = false;

    // refresh the page
    setTimeout(() => window.location.reload(), 800);

    message.success("Payment been confirmed");
  } catch (e) {
    console.log(e);
  }
};
</script>

<template>
  <n-space vertical>
    <n-h1>Orders</n-h1>
    <n-data-table
      remote
      :columns="columns"
      :data="orderList"
      striped
      :loading="loading"
      :pagination="pagination"
      @update:page="handlePageChange"
      @update:filters="handleFilterChange"
    ></n-data-table>
  </n-space>

  <!-- dialog for viewing specific order row -->
  <n-modal
    v-model:show="showView"
    preset="dialog"
    title="Order Details"
    style="width: 800px"
  >
    <n-descriptions
      label-placement="top"
      bordered
      :column="4"
      class="details-table"
    >
      <n-descriptions-item label="id" :span="2">
        {{ selectedRow.data.id }}
      </n-descriptions-item>
      <n-descriptions-item label="created_time" :span="2">
        {{ selectedRow.data.created_time }}
      </n-descriptions-item>
      <n-descriptions-item label="Campus">
        {{ selectedRow.data.campus.name }}
      </n-descriptions-item>
      <n-descriptions-item label="Course Name">
        {{ selectedRow.data.course.name }}
      </n-descriptions-item>
      <n-descriptions-item label="University Code">
        {{ selectedRow.data.course.uni_course_code }}
      </n-descriptions-item>
      <n-descriptions-item label="original_price">
        {{ selectedRow.data.original_price }}
      </n-descriptions-item>
      <n-descriptions-item label="paid">
        {{ selectedRow.data.paid }}
      </n-descriptions-item>
      <n-descriptions-item label="Paid Time" :span="2">
        {{ selectedRow.data.paid_time }}
      </n-descriptions-item>
      <n-descriptions-item label="Paid Price">
        {{ selectedRow.data.paid_price }}
      </n-descriptions-item>
      <n-descriptions-item label="Comment" :span="4">
        {{ selectedRow.data.paid_comment }}
      </n-descriptions-item>
    </n-descriptions>

    <template #action>
      <n-space
        ><n-button type="primary" @click="showView = false">
          Done
        </n-button></n-space
      >
    </template>
  </n-modal>
  <n-modal v-model:show="showConfirmPayment"
    ><n-card
      style="width: 400px"
      title="Confirm Payment"
      :bordered="false"
      size="huge"
    >
      <n-space vertical>
        <n-h1>Payment Details</n-h1>

        <!-- paymentForm is {}, paymentFormRef is null -->
        <n-form ref="paymentFormRef" :label-width="80" :model="paymentForm">
          <n-form-item label="Actual Payment" path="price">
            <n-input-number
              v-model:value="paymentForm.price"
              :show-button="false"
            >
              <template #prefix> $ </template>
            </n-input-number>
          </n-form-item>
          <n-form-item label="Comment" path="comment">
            <n-input v-model:value="paymentForm.comment" type="textarea" />
          </n-form-item>
        </n-form>
      </n-space>
      <template #footer>
        <n-space>
          <n-button type="primary" @click="confirmPayment">Confirm</n-button>
          <n-button @click="showConfirmPayment = false">Cancel</n-button>
        </n-space>
      </template>
    </n-card>
  </n-modal>
</template>

<style scoped>
.details-table {
  margin-top: 24px;
}
</style>
