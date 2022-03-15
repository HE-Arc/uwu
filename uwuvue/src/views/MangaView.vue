<template>
  <h1>{{manga.name}}</h1>

  <div v-if="manga.chapters.length > 0" class="row">
    <div v-for="(chapter, index) in manga.chapters" :key="index" class="col-6 col-md-3 col-lg-2">
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
