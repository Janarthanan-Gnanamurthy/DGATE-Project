<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <main class="flex bg-gray-100 min-h-screen">
    <!-- Adjust the Sidebar component as needed -->
    <Sidebar />

    <div class="flex-1 p-6">
      <h1 class="text-3xl font-semibold mb-6">Test Results</h1>
      <div class="bg-white rounded-lg shadow-md overflow-hidden overflow-y-auto max-h-svh">
        <table class="min-w-full table table-pin-rows">
          <thead >
            <tr class="bg-gray-800 text-white text-lg">
              <th class="w-1/12 py-3"></th>
              <th class="w-2/12 py-3">Test ID</th>
              <th class="w-2/12 py-3">Course</th>
              <th class="w-3/12 py-3">Topic</th>
              <th class="w-2/12 py-3">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!results[0]" class="text-2xl font-semibold text-center">
              <th></th>
              <th></th>
              <th></th>
              <th>No Test results available</th>
            </tr>
            <tr
              v-for="(result, index) in results"
              :key="index"
              class="hover:bg-gray-100 hover:cursor-pointer text-lg"
              @click="getTestResult(result.id)"
            >
              <th class="py-4">{{ index + 1 }}</th>
              <td class="py-4">{{ result.test_id }}</td>
              <td class="py-4">{{ result.metrics.course }}</td> <!-- Add actual course data -->
              <td class="py-4">{{ result.metrics.topic }}</td> <!-- Add actual topic data -->
              <td class="py-4">{{ result.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="showLoader" class="fixed z-50 inset-0 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen bg-black bg-opacity-15">
          <div class="loader-container">
            <div class="loader">
              <span class="loading loading-spinner loading-lg"></span>
            </div>
          </div>
        </div>
      </div>
  </main>
</template>

<script>
export default {
  data(){
    return {
      results: this.$store.state.results,
      showLoader: false
    }
  },
  methods: {
    async getTestResult(result_id) {
      try {
        this.showLoader=true
				await this.$store.dispatch('getTestResult', result_id);
        this.$router.push('/result');
			} catch (error) {
				console.error('Error in Fetching TestResult:', error);
			}
    }
  }
}
</script>
