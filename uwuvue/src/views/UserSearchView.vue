<template>
  <div class="row">
    <form @submit.prevent="searchPressed" class="col-md-9 col-lg-6">
      <div class="input-group mb-4">
          <input v-model="query" type="search" class="form-control" placeholder="Search users">
          
          <button class="btn btn-primary" type="button" disabled v-if="loading">
            <span class="spinner-border spinner-border-sm" role="status"></span>
            loading...
          </button>

          <button type="submit" class="btn btn-primary" v-else>search</button>
      </div>
    </form>
  </div>

  <div v-if="users.length > 0 || loading" class="row">
    <div v-for="(user, index) in users" :key="index" class="col-6 col-md-3 col-lg-2">
      <user-thumbnail :user="manga"/>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No result</div>
  </div>

  <button @click="moreResult" v-if="next" class="btn btn-primary">
    more results
  </button>
</template>

<script>
import api from '@/api'

import UserThumbnail from '@/components/UserThumbnail.vue'

export default {
  name : 'SearchView',

  components: {
    UserThumbnail
  },

  data() {
    return {
      users: [],
      query: this.$route.params.query,
      loading: false,
      next: null
    }
  },

  created() {
    this.search()

    this.$watch(
      () => this.$route.params,
      () => {
        this.search()
      }
    )
  },

  methods: {
    searchPressed() {
      this.$router.push({
        name: 'search',
        params: {
          query: this.query
        }
      })
    },

    search() {
      this.loading = true

      api.get('/uwusers/', {
        params: {
          search: this.$route.params.query
        },

        headers: this.$store.getters.header
      })
      .then(response => {
        this.users = response.data.results
        this.next = response.data.next
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
    },

    moreResult() {
      this.loading = true

      api.get(this.next, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.users.push.apply(this.users, response.data.results)
        this.next = response.data.next
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
    }
  },
}
</script>
