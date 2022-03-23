<template>
    <div>
        <router-link v-bind:to="'/users/'" + friend.id>
            <img v-bind:src="friend.image" class="img-fluid rounded-circle"/>
            <p class="p-1">{{friend.name}}</p>
        </router-link>
    </div>
</template>

<script>
export default {
    name: "FriendThumbnail",

    props: {
        friend : Object
    }

}
</script>

<style>

</style>