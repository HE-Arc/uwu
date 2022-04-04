<template>
 
    <div>
        <h1 class="text-primary">New friends requests</h1>
    </div>
  <p></p>
  <div v-if="friends.length > 0 || loading" class="row">
    <div v-for="(friend, index) in friends" :key="index" class="col-6 col-md-3 col-lg-2">
      <div>
        <p>{{friend.sender}}</p>
        <a @click.prevent="acceptFriend" type="button" class="btn btn-success me-3">Accept</a>
        <a @click.prevent="refuseFriend" type="button" class="btn btn-danger">Cancel</a>
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
      query: this.$route.params.query,
      loading: false,
      next: null
    }
  },

  created() {
    this.fetch()
  },

  methods: {
    fetch() {
      this.loading = true

      api.get(`/friend-requests/get_active_friend_request/`, {
        headers: this.$store.getters.header
      }) 
      .then(response => {
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

    acceptFriend() {

    },

    refuseFriend() {
      //console.log(this.friends[0])
      //api.delete(`/friend-requests/${this.friends.id}/`, {
      //  headers: this.$store.getters.sender.id
      //}) 
    }
  },
}
</script>
