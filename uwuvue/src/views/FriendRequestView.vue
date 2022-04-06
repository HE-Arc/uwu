<template>
 
    <div>
        <h1 class="text-primary">New friends requests</h1>
    </div>
  <p></p>
  <div v-if="friends.length > 0 || loading" class="row">
    <div v-for="(friend, index) in friends" :key="index" class="">
      <div class="mb-4">
        <router-link :to="'/users/' + friend.sender.pk"  class="text-primary text-decoration-none ms-3">{{friend.sender.username}}</router-link>
        <a @click.prevent="acceptFriend(friend.pk)" type="button" class="btn btn-success ms-3">Accept</a>
        <a @click.prevent="refuseFriend(friend.pk)" type="button" class="btn btn-danger ms-3">Cancel</a> 


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

//import UserThumbnail from '../components/UserThumbnail.vue'

export default {
  name : 'FriendRequest',

  components: {
   // UserThumbnail
  },

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
    api.get(`/uwuusers/${this.$route.params.id}/`, {
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

      api.get(`/friend-requests/get_active_friend_request/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        console.log(response)

        this.friends = response.data.results
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
     .catch(() => {
       console.log("can't accept invitation")
     })
      console.log(this.$store.getters.header)
    },

    refuseFriend(pkfriend) {
      api.post(`/friend-requests/${pkfriend}/decline/`, {}, {
        headers: this.$store.getters.header
      }) 
      .then(() => {
      this.fetch()
      })
     .catch(() => {
       console.log("can't cancel invitation")
     })
      console.log(this.$store.getters.header)
    }
  },
}
</script>
