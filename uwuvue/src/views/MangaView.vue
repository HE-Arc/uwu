<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <img :src="manga.image" class="img-fluid rounded mb-4"/>
    </div>

    <div class="col mb-4">
      <h1 class="text-primary">{{manga.name}}</h1>
      <p>{{manga.author}}</p>
      <p>{{manga.date}}</p>
    </div>
  </div>

  <div class="row mb-4">
    <div class="col">
      <div v-if="manga.progress != null" class="progress">
        <div :class="progressClass" :style="progressStyle" class="progress-bar" role="progressbar"/>
      </div>
    </div>
  </div>

  <div v-if="chapters.length > 0" class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4">
    <div v-for="(chapter, index) in chapters" :key="index" class="col">
      <chapter-button :chapter="chapter" v-on:toggle="fetch"/>
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
      manga: {},
      chapters: {}
    }
  },

  created() {
    this.fetch()
  },

  computed: {
    progressStyle: function() {
      return 'width: ' + this.manga.progress + '%'
    },

    progressClass: function() {
      if (this.manga.progress == 100) {
        return 'bg-primary'
      }

      return 'bg-info'
    }
  },

  methods: {
    fetch() {
      api.get(`/mangas/${this.$route.params.id}/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
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
