<template>
  <div class="row">
    <div class="col-12 col-md-8 col-lg-9">
      <user-title :user="user" :fromProfile="fromProfile" :large="true"/>
    </div>

    <div class="col">
      <div class="row">
        <router-link v-if="fromProfile && requestCount > 0" :to="$route.path + '/requests'" class="btn btn-primary mb-3">
          friend requests <span class="badge bg-dark">{{requestCount}}</span>
        </router-link>
      </div>
    </div>
  </div>

  <router-link :to="$route.path + '/readed'" type="button" class="text-decoration-none">
  <h2>Mangas readed</h2>
  </router-link>

  <div class="row"  v-if="readed.length > 0">
    <div v-for="(manga, index) in readed.slice(0, 6)" :key="index" class="col-6 col-md-3 col-lg-2">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No manga readed</div>
  </div>

  <router-link :to="$route.path + '/favorites'" type="button" class="text-decoration-none">
    <h2 class="mt-3">Favorites mangas</h2>
  </router-link>

  <div class="row gy-4 gx-3 gx-md-4"  v-if="favorites.length > 0">
    <div v-for="(manga, index) in favorites.slice(0, 6)" :key="index" class="col-6 col-md-3 col-lg-2">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>
  
  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No favorites manga</div>
  </div>

  <div v-if="fromProfile">
    <router-link :to="$route.path + '/friends'" class="text-decoration-none">
      <h2 class="mt-3">My Friends</h2>
    </router-link>

    <div class="row gy-4 gx-3 gx-md-4" v-if="friends.length > 0">
      <div v-for="(friends, index) in friends.slice(0, 6)" :key="index" class="col-6 col-md-3 col-lg-2">
        <user-thumbnail :user="friends"/>
      </div>
    </div>
  
    <div v-else class="row">
      <div class="alert alert-primary col-lg-6" role="alert">No friend :'(</div>
    </div>
  </div>
</template>

<script>
import api from '@/api'

import UserTitle from '@/components/UserTitle.vue'
import MangaThumbnail from '@/components/MangaThumbnail.vue'
import UserThumbnail from '@/components/UserThumbnail.vue'

export default {
  name : 'UserView',

  components: {
    MangaThumbnail,
    UserThumbnail,
    UserTitle
  },

  data() {
    return {
      user: {},
      favorites:[],
      readed:[],
      friends:[],
      requestCount: 0,
      fromProfile: this.$route.name == 'profile'
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
      api.get(`users/${this.user.pk}/get_favorites/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results) {
          this.favorites = response.data.results
        }
      })
      .catch(error => {
          console.log(error)
      })

      api.get(`users/${this.user.pk}/get_readed_mangas/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results) {
          this.readed = response.data.results
        }
      })
      .catch(error => {
        console.log(error)
      })

      api.get(`users/${this.user.pk}/get_friends/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results){
          this.friends = response.data.results
          this.friendNext = response.data.next
        }           
      })
      .catch(error => {
        console.log(error)
      })

      if (!this.fromProfile) {
        return;
      }

      api.get('/friend-requests/get_active_friend_request/', {
        headers: this.$store.getters.header
      })
      .then(response => {
        if (response.data.results) {
          this.requestCount = response.data.results.length
        }

        this.loading = false
      })
      .catch(() => {
        this.loading = false
      })
    }
  }
}
</script>
