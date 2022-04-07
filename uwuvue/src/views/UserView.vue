<template>
  <user-title :user="user" :fromProfile="fromProfile"/>

  <h2>Mangas readed</h2>

  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4"  v-if="readed.length > 0">
    <div v-for="(manga, index) in readed.slice(0, 6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>
      
  <router-link v-if="readed.length > 0" :to="$route.path + '/readed'" type="button" class="btn btn-primary">more</router-link>

  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No manga readed</div>
  </div>

  <h2 class="mt-5">Favorites mangas</h2>

  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4"  v-if="favorites.length > 0">
    <div v-for="(manga, index) in favorites.slice(0, 6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>

  <router-link v-if="favorites.length > 0" :to="$route.path + '/favorites'" type="button" class="btn btn-primary">more</router-link>
  
  <div v-else class="row">
    <div class="alert alert-primary col-lg-6" role="alert">No favorites manga</div>
  </div>

  <div v-if="fromProfile">
    <h2 class="mt-5">My Friends</h2>

    <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4" v-if="friends.length > 0">
      <div v-for="(friends, index) in friends.slice(0, 6)" :key="index" class="col">
        <user-thumbnail :user="friends"/>
      </div>
    </div>

    <router-link v-if="friends.length > 0" :to="$route.path + '/friends' " type="button" class="btn btn-primary">more</router-link>
  
    <div v-else class="row">
      <div class="alert alert-primary col-lg-6" role="alert">No friends :'(</div>
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
      pages : null,
      fromProfile: this.$route.name == 'profile'
    }
  },

  created() {
    this.$watch(
      () => this.$route.name,
      () => {
        if (this.$route.name == 'users' || this.$route.name == 'profile')
        {
          this.fromProfile = this.$route.name == 'profile'
          this.fetchUser()
        }
      }
    )

    this.fetchUser()
  },

  methods: {
    fetchUser() {
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

    fetch() {
      api.get(`users/${this.user.pk}/get_favorites/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.favorites = []

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
        this.readed = []

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
        this.friends = []

        if (response.data.results){
          this.friends = response.data.results
          this.friendNext = response.data.next
        }           
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
