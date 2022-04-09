<template>
  <div class="row">
    <div :class="colSize">
      <friend-icon v-if="!fromProfile && $store.getters.isLogged" :user="user"/>
      <img :src="user.image" class="img-fluid rounded mb-4"/>
    </div>

    <div class="col mb-4">
      <h1 class="text-primary">{{user.username}}</h1>
      <h4>Pages readed: {{pages}}</h4>
    </div>
  </div>
</template>

<script>
import api from '@/api'

import FriendIcon from '@/components/FriendIcon.vue'

export default {
  name: 'UserTitle',

  components: {
    FriendIcon
  },

  props: {
    user: Object,
    fromProfile: Boolean,
    large: Boolean
  },

  data() {
    return {
      pages: 0
    }
  },

  computed: {
    colSize: function() {
      if (this.large) {
        return 'col-4 col-md-3'
      }

      return 'col-4 col-md-2'
    }
  },

  created() {
    this.$watch(
      () => this.user,
      () => {
        this.fetch()
      }
    )
  },

  methods: {
    fetch() {
      api.get(`users/${this.user.pk}/total_pages_readed/`, {
        headers: this.$store.getters.header
      })
      .then(response => {
        this.pages = response.data.pages_readed       
      })
      .catch(error => {
          console.log(error)
      })
    }
  }
}
</script>