<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <favorite-icon :manga="manga"/>
      <img :src="manga.image" class="img-fluid rounded mb-4"/>
    </div>

    <div class="col mb-4">
      <h1 class="text-primary">{{manga.name}}</h1>
      <p>{{manga.author}} - {{manga.date}}</p>
      <p>{{manga.description}}</p>
    </div>
  </div>

  <div class="row mb-4">
    <div class="col">
      <progress-bar :manga="manga"/>
    </div>
  </div>

  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4">
    <div v-for="(chapter, index) in chapters" :key="index" class="col">
      <chapter-button :chapter="chapter" @toggle="fetch"/>
    </div>
  </div>
</template>

<script>
import api from '@/api'

import ChapterButton from '@/components/ChapterButton.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import FavoriteIcon from '@/components/FavoriteIcon.vue'

export default {
  name : 'MangaView',

  components: {
    ChapterButton,
    ProgressBar,
    FavoriteIcon
  },

  data() {
    return {
      manga: {},
      chapters: {}
    }
  },

  created() {
    this.fetch()
  },

  methods: {
    fetch() {
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

      api.get(`/mangas/${this.$route.params.id}/get_chapters/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.chapters = response.data
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
