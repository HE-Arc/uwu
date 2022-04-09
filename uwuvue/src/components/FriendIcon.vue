<template>
  <div class="position-relative" @mouseover="isMouseOver = true" @mouseleave="isMouseOver = false">
    <a @click.prevent="askFriend" :class="friendClass" href="ask-friend" v-if="$store.getters.isLogged" 
        class="position-absolute m-2 top-0 start-0 fs-3" role="img"/>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'FriendIcon',

  props: {
    user: Object
  },

  data() {
    return {
      isAsked: this.user.isAsked,
      isFriend: this.user.isFriend,
      isMouseOver: false
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

  computed: {
    friendClass: function() {
      if (this.isFriend) {
        if (this.isMouseOver) {
          return "bi bi-person-x-fill"
        }

        return "bi bi-person-hearts"
      }

      if (this.isAsked) {
        if (this.isMouseOver) {
          return "bi bi-person-x-fill"
        }

        return "bi bi-person-check-fill"
      }

      return "bi bi-person-plus"
    }
  },

  methods: {
    fetch() {
      api.get(`/users/${this.user.pk}/is_friend/`, {
        headers: this.$store.getters.header
      })
      .then((response) => {
        this.isAsked = response.data.is_asked;
        this.isFriend = response.data.is_friend;
      })
    },

    askFriend() {
      if (this.isAsked) {
        api.post(`/users/${this.user.pk}/cancel_friend/`, {}, {
          headers: this.$store.getters.header
        })
        .then(() => {
          this.isAsked = false;
        })

        return
      }

      if (!this.isFriend) {
        api.post(`/users/${this.user.pk}/ask_friend/`, {}, {
          headers: this.$store.getters.header
        })
        .then(() => {
          this.isAsked = true;
        })

        return
      }
      
      api.post(`/users/${this.user.pk}/unfriend/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.isAsked = false;
        this.isFriend = false;
      })
    },
  }
}
</script>
