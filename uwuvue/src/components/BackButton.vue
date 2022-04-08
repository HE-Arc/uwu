<template>
  <button v-if="visible" @click="goBack" class="m-4 btn btn-primary position-fixed">
    <i class="bi bi-arrow-left"/>
  </button>
</template>

<script>
export default {
  name : 'BackButton',

  data() {
    return {
      visible: this.$route.name != 'home'
    }
  },

  created() {
    this.$watch(
      () => this.$route.name,
      () => {
        this.visible = this.$route.name != 'home'
      }
    )
  },

  methods: {
    goBack() {
      this.$router.back()
      this.visible = false
    }
  }
}
</script>
