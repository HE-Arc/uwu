<template>
  <user-title :user="user" :fromProfile="fromProfile"/>

  <div>
    <h1>All mangas readed</h1>
  </div>

  <div v-if="mangas.length > 0 || loading" class="row">
    <div v-for="(manga, index) in mangas" :key="index" class="col-6 col-md-3 col-lg-2">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No result</div>
  </div>

  <div v-if="next" class="text-center">
    <button @click="moreResult" class="btn btn-primary mt-4">
      more results
    </button>
  </div>
</template>

<script>
import api from '@/api'

import MangaThumbnail from '@/components/MangaThumbnail.vue'
import UserTitle from '@/components/UserTitle.vue'

export default {
  name : 'ReadedView',

  components: {
    MangaThumbnail,
    UserTitle
  },

  data() {
    return {
      mangas: [],
      query: this.$route.params.query,
      order: '',
      loading: false,
      next: null,
      user: {},
      fromProfile: this.$route.name == 'profile-readed'
    }
  },

  created() {
    if (this.fromProfile) {
      api.get('/users/my_user/', {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.user = response.data
        this.fetch()
      })
      .catch(() => {
        this.$router.push('/404')
      })
    }
    else {
      api.get(`/users/${this.$route.params.id}/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.user = response.data
        this.fetch()
      })
      .catch(() => {
        this.$router.push('/404')
      })
    }
  },

  methods: {
    fetch() {
      this.loading = true

      api.get(`/users/${this.user.pk}/get_readed_mangas/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results) {
          this.mangas = response.data.results
          this.next = response.data.next
        }

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
