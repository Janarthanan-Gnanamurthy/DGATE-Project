<template>
	<div class="menu flex flex-col bg-primary-content min-w-96 pt-8 p-0 h-screen" >
		<ul>
		<li class="mb-0.5"><RouterLink to="/" class="btn text-2xl border-0 ">Courses</RouterLink></li>
		<li class="mb-0.5"><RouterLink to="/dashboard" class="btn text-2xl border-0 ">Dashboard</RouterLink></li>
		<li class="mb-0.5"><div @click="redirect" class="btn text-2xl border-0 ">Scores</div></li></ul>
	</div>
</template>

<script>
export default {
	methods: {
		async redirect(){
			await this.$store.dispatch('getResults')

			this.$router.push('/scores')
		}
	}
}
</script>

<style scoped>
a.router-link-active {
	border:  solid 2px violet;
}
</style>