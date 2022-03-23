<template>
    <div class="profile--page">
            <h1>My profil</h1>
            <div class="profile--informations">
                <div class="profile--image col-md-6 mb-4">
                    <!-- <img v-bind:src="user.image" class="img-fluid rounded mb-3"/> -->
                </div>
                <p>Username uWu</p>
                <p>Birth</p>
                <div class="manga--list">

                      <MangaThumbnailRow />           
                
                </div>
                    <div class="friend--list">
                        <h2>Friends</h2>

                       
                    </div>
            </div>
    </div>
</template>

<script>
import api from '@/api'
import MangaThumbnailRow from '@/components/MangaThumbnailRow.vue'

export default {
    name: 'ProfilePage',

    components: {
        MangaThumbnailRow,
    },
    methods: {
    }, 
    

    created() {
      api.get('/profile/', {
        headers: this.$store.getters.header
      })
      .then(response => {
        console.log(response.data.results)
        this.mangas = response.data.results
      })
      .catch(error => {
        console.log(error.response.data)
      })
    },

    search() {
      this.loading = true

      api.get('/mangas/', {

        headers: this.$store.getters.header
      })
      .then(response => {
        this.mangas = response.data.results
        this.loading = false
      })
      .catch(() =>
        this.loading = false
      )
    }

}
</script>

<style>
    .profile--informations {
        
    

    }

    .profile--image {
           width: 100px;
           height: auto;

        }


    
    
    
</style>