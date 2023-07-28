<script setup>
const props = defineProps({
  header: String,
  head_end: String,
  message: Number,
  type: String,
});

defineEmits(['closeToast'])
</script>

<template>
<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
  <div id="liveToast" class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <img src="@/assets/blue.svg" class="rounded me-2" alt="Info" v-if="type=='info'">
      <img src="@/assets/red.svg" class="rounded me-2" alt="Info" v-if="type=='error'">
      <strong class="me-auto">{{ props.header }}</strong>
      <small>{{ props.head_end }}</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close" @click="$emit('closeToast')"></button>
    </div>
    <div class="toast-body placeholder-glow">
      <div class="spinner-border text-primary" role="status" v-if="props.message==''">
        <span class="visually-hidden">Loading...</span>
      </div>
      {{ props.message }}
    </div>
  </div>
</div>
</template>