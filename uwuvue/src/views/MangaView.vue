<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <img v-bind:src="manga.image" class="img-fluid rounded mb-3"/>
    </div>

    <div class="col">
      <h1 class="text-primary">{{manga.name}}</h1>
      <p>{{manga.author}}</p>
      <p>{{manga.date}}</p>
    </div>
  </div>

  <div class="row">
    <div v-if="manga.progress && manga.progress > 0" class="progress">
      <div v-if="manga.progress == 100" v-bind:style="progressStyle()" class="progress-bar bg-info progress-bar-striped" role="progressbar"/>
      <div v-else v-bind:style="progressStyle()" class="progress-bar bg-info" role="progressbar"/>
    </div>
  </div>

  <div v-if="manga.chapters.length > 0" class="row">
    <div v-for="(chapter, index) in manga.chapters" :key="index" class="col-4 col-md-3 col-lg-2">
      <chapter-button :chapter="chapter"/>
    </div>
  </div>
</template>

<script>
import api from '@/api'

import ChapterButton from '@/components/ChapterButton.vue'

export default {
  name : 'MangaView',

  components: {
    ChapterButton
  },

  data() {
    return {
      manga: {}
    }
  },

  created() {
      api.get(`/mangas/${this.$route.params.id}/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        console.log(response.data)
        this.manga = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>
