<template>
  <div class="position-relative">
    <a @click.prevent="askFriend" :class="friendClass" href="ask-friend" v-if="$store.getters.isLogged && !isFriend && !isAsked" 
      class="position-absolute m-2 top-0 start-0 fs-3" role="img"/>
     <a :class="friendClass" href="ask-friend" v-if="$store.getters.isLogged && this.isAsked || this.isFriend" 
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
      isFriend : this.user.isFriend
    }
  },

  created() {
    this.$watch(
      () => this.user,
      () => {
        this.isFriend = this.user.isFriend
        this.isAsked = this.user.isAsked
      }
    )
  },

  computed: {
    friendClass: function() {
      if (this.isFriend) {
        return "bi bi-person-hearts"
      }

      if (this.isAsked) {
        return "bi bi-person-check-fill"
      }

      return "bi bi-person-plus"
    }
  },

  methods: {
    askFriend() {
      api.post(`/users/${this.user.pk}/ask_friend/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.isAsked = true;
      })
    },

    cancelFriend() {
      api.post(`/uwuusers/${this.user.pk}/unfriend/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.isAsked = false;
        this.isFriend = false;
      })
    },

    areFriend() {
     api.post(`/users/${this.user.pk}/is_friend/`, {}, {
        headers: this.$store.getters.header
      })
      .then(() => {
        this.isAsked = false;
        this.isFriend = true;
      })
    }
  }
}
</script>
