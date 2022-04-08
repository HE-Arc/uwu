<template>
  <user-title :user="user" :fromProfile="true"/>

  <div>
      <h1>All my friends</h1>
  </div>

  <div v-if="friends.length > 0 || loading" class="row">
    <div v-for="(friend, index) in friends" :key="index" class="col-6 col-md-3 col-lg-2">
      <user-thumbnail :user="friend"/>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No friend :'(</div>
  </div>

  <div v-if="next" class="position-relative">
    <button @click="moreResult" class="btn btn-primary mt-4 position-absolute top-0 start-50 translate-middle">
      more results
    </button>
  </div>
</template>

<script>
import api from '@/api'

import UserThumbnail from '../components/UserThumbnail.vue'
import UserTitle from '../components/UserTitle.vue'

export default {
  name : 'UserFriendsView',

  components: {
    UserThumbnail,
    UserTitle
  },

  data() {
    return {
      friends: [],
      query: this.$route.params.query,
      order: '',
      loading: false,
      next: null,
      user: {}
    }
  },

  created() {
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
  },

  methods: {
    fetch() {
      this.loading = true

      api.get(`/users/${this.user.pk}/get_friends/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results) {
          this.friends = response.data.results
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
        this.friends.push.apply(this.friends, response.data.results)
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
