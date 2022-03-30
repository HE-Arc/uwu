<template>
  <div class="row">
    <div class="col-4 col-md-2">
      <friend-icon :user="user"/>
      <img :src="user.image" class="img-fluid rounded mb-4"/>
    </div>

    <div class="col mb-4">
      <h1 class="text-primary">{{user.username}}</h1>
    </div>
  </div>

   <h2>Mangas readed</h2>

  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4 flex-nowrap overflow-auto">
    <div v-for="(manga, index) in readed.slice(0,6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>
      <div>
           <router-link :to="'/users/' + user.pk + '/readed'" type="button" class="btn btn-primary">more...</router-link>
      </div> 

  <h2>Favorites mangas</h2>

  <div class="row row-cols-3 row-cols-md-4 row-cols-lg-6 gy-4 gx-3 gx-md-4 flex-nowrap overflow-auto">
    <div v-for="(manga, index) in favorites.slice(0,6)" :key="index" class="col">
      <manga-thumbnail :manga="manga" :simple="true"/>
    </div>
  </div>
      <div>
           <router-link :to="'/users/' + user.pk + '/favorites'" type="button" class="btn btn-primary">more...</router-link>
      </div>


  

</template>

<script>
import api from '@/api'

import MangaThumbnail from '@/components/MangaThumbnail.vue'
import FriendIcon from '@/components/FriendIcon.vue'


export default {
  name : 'UserView',

  components: {
    MangaThumbnail,
    FriendIcon
  },

  data() {
    return {
      user: {},
      favorites:[],
      readed:[],
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

    api.get(`/users/${this.$route.params.id}/get_favorites/`, {
        headers: this.$store.getters.header
    })
    .then(response => {
        this.favorites = response.data
    })
    .catch(error => {
        console.log(error)
    })

    
     api.get(`/users/${this.$route.params.id}/get_readed/`, {
        headers: this.$store.getters.header
    })
    .then(response => {
        this.readed = response.data
    })
    .catch(error => {
        console.log(error)
    })

  }
}
</script>
