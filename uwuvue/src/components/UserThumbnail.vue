<template>
  <div>
    <router-link :to="'/users/' + user.pk">
      <img :src="user.image" class="img-fluid rounded mb-5"/>
    </router-link>

    <p class="p-1">{{user.name}}</p>
  </div>
</template>

<script>
export default {
  name: 'UserThumbnail',

  props: {
    user: Object
  }
}
</script>