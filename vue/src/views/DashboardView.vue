<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <main class="flex bg-gray-100 min-h-screen">
    <Sidebar />
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-8 text-center">Progress Report</h1>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- User Information -->
        <div class="bg-base-200 rounded-lg p-6 shadow-md">
          <h2 class="text-xl font-bold mb-4">User Information</h2>
          <div class="text-sm">
            <p>Name: {{ user.name }}</p>
            <p>Email: {{ user.email }}</p>
            <p>Department: {{ user.department }}</p>
          </div>
        </div>

        <!-- Course Progress -->
        <div class="bg-base-200 rounded-lg p-6 shadow-md">
          <h2 class="text-xl font-bold mb-4">Course Progress</h2>
          <div v-for="course in courses" :key="course.id" class="text-sm">
            <p>Course: {{ course.title }}</p>
            <progress
              class="progress progress-primary w-full"
              :value="calculateCourseProgress(course)"
              max="100"
            >
              {{ calculateCourseProgress(course) }}%
            </progress>
          </div>
        </div>

        <!-- Test Results -->
        <div class="bg-base-200 rounded-lg p-6 shadow-md h-2/3 overflow-auto">
          <h2 class="text-xl font-bold mb-4">Test Results</h2>
          <div v-if="results && results.length > 0" class="text-sm">
            <div v-for="result in results" :key="result.id" class="mb-4">
              <p>Test: {{ result.test_id }}</p>
              <progress
                class="progress progress-success w-full"
                :value="result.score"
                max="100"
              >
                {{ result.score }}%
              </progress>
            </div>
          </div>
          <p v-else class="text-sm">No test results available</p>
        </div>
      </div>

      <!-- Topic Progress -->
      <div v-if="course && course.topics" class="mt-8 bg-base-200 rounded-lg p-6 shadow-md">
        <h2 class="text-xl font-bold mb-4">Topic Progress</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="topic in course.topics" :key="topic.id" class="text-sm">
            <p class="font-semibold">{{ topic.title }}</p>
            <progress
              class="progress progress-info w-full"
              :value="calculateTopicProgress(topic)"
              max="100"
            >
              {{ calculateTopicProgress(topic) }}%
            </progress>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState([
      'user',
      'course',
      'courses',
      'results',
    ]),
  },
  methods: {
    calculateCourseProgress(course) {
      if (!course || !course.topics) return 0;

      const totalTopics = course.topics.length;
      const completedTopics = course.topics.filter(
        (topic) => this.calculateTopicProgress(topic) === 100
      ).length;

      return (completedTopics / totalTopics) * 100;
    },
    calculateTopicProgress(topic) {
      if (!topic || !topic.questions || !topic.test) return 0;

      const totalQuestions = topic.questions.length;
      const completedQuestions = topic.test.questions.length;

      return (completedQuestions / totalQuestions) * 100;
    },
  },
};
</script>