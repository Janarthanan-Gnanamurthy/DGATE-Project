<template>
  <div class="p-10">
    <h2 class="text-3xl mb-5">Create Test</h2>
    <div class="text-2xl">
      <label for="course-select">Select Course:</label>
      <select id="course-select" v-model="selectedCourse" @change="fetchTopics">
        <option value="">Select Course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.title}}</option>
      </select>
    </div>
    <div v-if="topics.length > 0">
      <label for="topic-select">Select Topic:</label>
      <select id="topic-select" v-model="selectedTopic" @change="fetchQuestions">
        <option value="">Select Topic</option>
        <option v-for="topic in topics" :key="topic.id" :value="topic.id">{{ topic.title }}</option>
      </select>
    </div>
    <div v-if="questions.length > 0">
      <table>
        <thead>
          <tr>
            <th>Select</th>
            <th>Question</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id">
            <td>
              <input type="checkbox" v-model="selectedQuestions" :value="question.id" />
            </td>
            <td>{{ question.text }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="createTest">Create Test</button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'CreateTest',
  data() {
    return {
      selectedCourse: '',
      selectedTopic: '',
      selectedQuestions: [],
      topics: [],
      questions: [],
    };
  },
  computed: {
    ...mapState(['courses']),
  },
  async created() {
    await this.$store.dispatch('getCourses');
  },
  methods: {
    ...mapActions(['getCourses', 'getCourse']),
    fetchTopics() {
      if (this.selectedCourse) {
        this.getCourse(this.selectedCourse)
          .then((course) => {
            this.topics = course.topics;
            this.selectedTopic = '';
            this.questions = [];
          })
          .catch((error) => {
            console.error('Error fetching topics:', error);
          });
      } else {
        this.topics = [];
        this.selectedTopic = '';
        this.questions = [];
      }
    },
    fetchQuestions() {
      if (this.selectedTopic) {
        // Fetch questions for the selected topic from the server
        // and update the `questions` data property
        // Example implementation:
        this.questions = [
          { id: 1, text: 'Question 1' },
          { id: 2, text: 'Question 2' },
          { id: 3, text: 'Question 3' },
        ];
      } else {
        this.questions = [];
      }
    },
    // createTest() {
    //   // Send the selected course, topic, and questions to the server
    //   // Example implementation:
    //   const testData = {
    //     courseId: this.selectedCourse,
    //     topicId: this.selectedTopic,
    //     questionIds: this.selectedQuestions,
    //   };

    //   fetch('/api/tests', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(testData),
    //   })
    //     .then((response) => {
    //       if (response.ok) {
    //         // Handle successful test creation
    //         console.log('Test created successfully');
    //         // You can navigate to a different page or show a success message here
    //       } else {
    //         // Handle error
    //         console.error('Error creating test');
    //       }
    //     })
    //     .catch((error) => {
    //       console.error('Error creating test:', error);
    //     });
    // },
  },
};
</script>