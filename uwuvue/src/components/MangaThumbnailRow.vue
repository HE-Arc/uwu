<template>
  <div class="manga--row">
      <h2>Collection</h2>
      <div class="manga--list">
          <!-- FAIRE LE V-FOR ICI -->
      </div>
  </div>
</template>

<script>
import MangaThumbnail from "./MangaThumbnail.vue"
export default {
    name: "MangaThumbnailRow",
    components : {
        MangaThumbnailRow,
    },
    props: {
        threeManga : Array
    },
    
}
</script>

<style>
    .manga--list {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>