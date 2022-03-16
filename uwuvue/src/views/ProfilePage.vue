<template>
    <div class="profile--page">
            <h1>My profil</h1>
            <div class="profile--informations">
                <div class="profile--image col-md-6 mb-4">
                    <img class="rounded-circle z-depth-2" src="https://ilarge.lisimg.com/image/23099837/820full-nezuko-kamado.jpg" data-holder-rendered="true">
                </div>
                
                <p>Username uWu</p>
                <p>Birth</p>
                <!-- ICI BOUTON POUR AJOUTER EN AMI DANS L'AUTRE VUE -->
                
                <div class="manga--list">
                    <h2>Collections</h2>

                    <button>Haha...</button>
                </div>
                    <div class="friend--list">
                        <h2>Friends</h2>

                        <button>Lool...</button>
                    </div>
            </div>
    </div>
</template>

<script>
import api from '@/api'

//import MangaThumbnailRow from '@/component/MangaThumbnailRow.vue'

export default {
    name: 'ProfilePage',

    components: {
     //   MangaThumbnailRow
    },
    
  /*  methods: {
        makeDataManga(){

        }
    }, */
    

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

    h2 {
        color: rosybrown;
    }

    
    
    
</style>