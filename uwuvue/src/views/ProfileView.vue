<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <img :src="user.image" class="img-fluid rounded mb-4"/>
    </div>
    <div class="col mb-4">
      <h1 class="text-primary">{{user.username}}</h1>
    </div>
  </div>
   <h2>Mangas readed</h2>
  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4"  v-if="readed.length > 0">
    <div v-for="(manga, index) in readed.slice(0,6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div> 
  </div>
      
    <router-link v-if="readed.length > 0" :to="'/users/' + user.pk + '/readed'" type="button" class="btn btn-primary">more...</router-link>

    <div v-else class="row">
      <div class="alert alert-primary col-lg-6" role="alert">No manga readed</div>
    </div>


  <h2 class="mt-5">Favorites mangas</h2>
  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4"  v-if="favorites.length > 0">
    <div v-for="(manga, index) in favorites.slice(0,6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>
    <router-link v-if="favorites.length > 0" :to="'/users/' + user.pk + '/favorites'" type="button" class="btn btn-primary">more...</router-link>
    <div v-else class="row">
      <div class="alert alert-primary col-lg-6" role="alert">No favorites manga</div>
    </div>

<h2 class="mt-5">My Friends</h2>
  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4" v-if="friends.length > 0">
    <div v-for="(friends, index) in friends.slice(0,6)" :key="index" class="col">
      <user-thumbnail :user="friends"/>
    </div>
  </div>
     <router-link v-if="friends.length > 0" :to="'/users/' + user.pk + '/friends' " type="button" class="btn btn-primary">more...</router-link>
     <div v-else class="row">
      <div class="alert alert-primary col-lg-6" role="alert">No friends :'(</div>
    </div>
  


</template>

<script>
import api from '@/api'

import MangaThumbnail from '@/components/MangaThumbnail.vue'
import UserThumbnail from '@/components/UserThumbnail.vue'

export default {
  name : 'ProfileView',

  components: {
    MangaThumbnail,
    UserThumbnail
  },

  data() {
    return {
      user: {},
      favorites:[],
      readed:[],
      friends:[],
      readedNext: null,
      favoriteNext: null,
      friendNext: null,
    }
  },

  created() {
    api.get(`/users/my_user/`, {
      headers: this.$store.getters.header
    })
    .then(response => {
      this.user = response.data
      this.fetch()
    })
    .catch(error => {
      console.log(error)
    })

    

    
    

  },

  methods: {
      fetch() {
        api.get(`users/${this.user.pk}/get_favorites/`, {
        headers: this.$store.getters.header
         })
    
        .then(response => {
            if(response.data.results) {
                this.favorites = response.data.results
                this.favoriteNext = response.data.next
            }
        })
    
        .catch(error => {
            console.log(error)
        })

        api.get(`users/${this.user.pk}/get_readed_mangas/`, {
        headers: this.$store.getters.header
        })
        
        .then(response => {
            if(response.data.results){
            this.readed = response.data.results
            this.readedNext = response.data.next
            }
            
        })
    
        .catch(error => {
            console.log(error)
        })

        api.get(`users/${this.user.pk}/get_friends/`, {
        headers: this.$store.getters.header
        })
        
        .then(response => {
            if(response.data.results){
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
