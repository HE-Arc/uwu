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

  <div v-if="users.length > 0 || loading || $route.params.query.trim().length == 0" class="row">
    <div v-for="(user, index) in users" :key="index" class="col-6 col-md-3 col-lg-2">
      <user-thumbnail :user="user"/>
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

import UserThumbnail from '@/components/UserThumbnail.vue'

export default {
  name : 'UserSearchView',

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
  },

  methods: {
    searchPressed() {
      this.$router.push({
        name: 'users-search',
        params: {
          query: this.query
        }
      })
    },

    search() {
      if (this.$route.params.query.trim().length == 0) {
        return
      }

      this.loading = true

      api.get('/users/', {
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
      .catch((error) => {
        console.log(error)
        this.loading = false
      })
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
      .catch(() => {
        this.loading = false
      })
    }
  },
}
</script>
