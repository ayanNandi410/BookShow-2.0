<script setup>
const props = defineProps({
  header: String,
  head_end: String,
  message: Number,
  type: String,
});
</script>

<template>
<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
  <div id="liveToast" class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <img src="..." class="rounded me-2" alt="...">
      <strong class="me-auto">{{ props.header }}</strong>
      <small>{{ props.head_end }}</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      {{ props.message }}
    </div>
  </div>
</div>
</template>