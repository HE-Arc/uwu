<template>
    <div>
        <h1>Mangas readed</h1>
    </div>
  <div v-if="mangas.length > 0 || loading" class="row">
    <div v-for="(manga, index) in mangas" :key="index" class="col-6 col-md-3 col-lg-2">
      <manga-thumbnail :manga="manga"/>
    </div>
  </div>
  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No result</div>
  </div>

  <div v-if="next" class="position-relative">
    <button @click="moreResult" class="btn btn-primary mt-4 position-absolute top-0 start-50 translate-middle">
      more results
    </button>
  </div>
</template>

<script>
import api from '@/api'

import MangaThumbnail from '@/components/MangaThumbnail.vue'

export default {
  name : 'ReadedView',

  components: {
    MangaThumbnail
  },

  data() {
    return {
      mangas: [],
      query: this.$route.params.query,
      order: '',
      loading: false,
      next: null
    }
  },

  created() {
    this.search()
  },

  methods: {
    search() {
      this.loading = true

      api.get(`/users/${this.$route.params.id}/get_readed_mangas/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas = response.data.results
        this.next = response.data.next
        this.loading = false
      })
      .catch(() => {
        this.loading = false
      })
    },

    moreResult() {
      this.loading = true

      api.get(this.next, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas.push.apply(this.mangas, response.data.results)
        this.next = response.data.next
        this.loading = false
      })
      .catch(() => {
        this.loading = false
      })
    }
  },
}
</script>
