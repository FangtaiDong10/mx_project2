<template></template>
<script setup>
import { useMessage } from "naive-ui";
//store the JS obejct which created by useMessage() to the browser's $message variable
window["$message"] = useMessage();
</script>
