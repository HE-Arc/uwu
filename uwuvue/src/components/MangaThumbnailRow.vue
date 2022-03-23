<template>
  <div class="manga--row">
      <h2>Collection</h2>
      <div class="manga--list">
         <manga-thumbnail v-for="(manga, index) in mangas" :key="index" :manga="manga"/> 

           <!--  <div v-for="(manga, index) in mangas" :key="index" class="col-6 col-md-3 col-lg-2">
                <manga-thumbnail :manga="manga"/>
            </div> -->

      </div>
      <button>More...</button>
  </div>
</template>

<script>
import MangaThumbnail from "./MangaThumbnail.vue"

export default {
    name: "MangaThumbnailRow",

    components : {
        MangaThumbnail,
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