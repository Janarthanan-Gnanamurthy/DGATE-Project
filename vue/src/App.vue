<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div>
    <!-- <HelloWorld msg="You did it!" /> -->

    <nav class="navbar bg-primary p-5 justify-between">
      <RouterLink to="/" class="text-2xl font-bold text-white">Placement Module</RouterLink>
      <button class="btn btn-primary" @click="keycloak.logout" >Log out</button>
    </nav>
    <RouterView />
  </div>
</template>


<script>
import keycloak from './keycloak'

export default {
  components: { Sidebar },
  data(){
    return {
      courses: this.$store.state.courses,
      showsidebar: false,
    }
  },
  methods: {

  },
  beforeCreate(){
    this.$store.dispatch('getCourses')
  }
}

</script>

