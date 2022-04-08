<template>
  <div>
    <h1 class="text-primary">New friends requests</h1>
  </div>

  <div v-if="friends.length > 0 || loading" class="row">
    <div v-for="(friend, index) in friends" :key="index">
      <div class="mb-4 card bg-dark">
        <div class="card-body d-flex">
          <h5 class="card-title">
            <router-link :to="'/users/' + friend.sender.pk"  class="link-primary text-decoration-none">{{friend.sender.username}}</router-link>
          </h5>
          <button @click.prevent="acceptFriend(friend.pk)" class="btn btn-primary ms-auto">accept</button> 
          <button @click.prevent="refuseFriend(friend.pk)" class="btn btn-info ms-3">cancel</button> 
        </div>
      </div>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No new requests :(</div>
  </div>

  <div v-if="next" class="position-relative">
    <button @click="moreResult" class="btn btn-primary mt-4 position-absolute top-0 start-50 translate-middle">
    more results
    </button>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name : 'FriendRequest',

  data() {
    return {
      friends: [],
      users: {},
      query: this.$route.params.query,
      loading: false,
      next: null
    }
  },

  created() {
    api.get('/users/my_user/', {
      headers: this.$store.getters.header
    })
    .then(response => {
      this.user = response.data
    })
    .catch(error => {
      console.log(error)
    })

    this.fetch()
  },

  methods: {
    fetch() {
      this.loading = true

      api.get('/friend-requests/get_active_friend_request/', {
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
    },

    acceptFriend(pkfriend) {
      api.post(`/friend-requests/${pkfriend}/accept/`, {}, { 
        headers: this.$store.getters.header
      })
      .then(() => {
        this.fetch()
      })
      .catch(error => {
       console.log(error)
      })
    },

    refuseFriend(pkfriend) {
      api.post(`/friend-requests/${pkfriend}/decline/`, {}, {
        headers: this.$store.getters.header
      }) 
      .then(() => {
        this.fetch()
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
}
</script>
