<template>
  <div class="p-10">
    <h2 class="text-3xl mb-5">Create Test</h2>
    <div>
      <label for="">Enter a Name for the Test:</label>
      <input type="text" v-model="testName" placeholder="Enter Test name">
    </div>
    <div class="text-2xl">
      <label for="course-select">Select Course:</label>

      <select id="course-select" v-model="selectedCourse" @change="fetchTopics">
        <option value="">Select Course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.title}}</option>
      </select>
    </div>
    <div v-if="topics.length > 0">
      <label for="topic-select">Select Topic:</label>
      {{ selectedTopic }}
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
            <th>Q.ID</th>
            <th>Question</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id">
            <td>
              <input type="checkbox" v-model="selectedQuestions" :value="question.id" />
            </td>
            <td>{{ question.id }}</td>
            <td>{{ question.statement }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="createTest" class="btn btn-primary">Create Test</button>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'CreateTest',
  data() {
    return {
      testName: '',
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
    async fetchQuestions() {
      this.selectedQuestions =[];
      if (this.selectedTopic) {
        try{
				  const response = await fetch(`http://localhost:8000/select-questions/${this.selectedTopic}`)
				if (!response.ok){
					throw new Error(`HTTP error! Status: ${response.status}`)
				}
				const data = await response.json();
        this.questions = data

        }catch (error) {
          console.error('Error fetching questions:', error);
          alert('Error fetching questions. Please try again.');
        }
      } else {
        this.questions = [];
      }
    },
    createTest() {
      // Send the selected course, topic, and questions to the server
      // Example implementation:
      const testData = {
        name: this.testName,
        topic_id: this.selectedTopic,
        question_ids: this.selectedQuestions,
      };

      fetch('http://localhost:8000/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData),
      })
        .then((response) => {
          if (response.ok) {
            // Handle successful test creation
            this.testName = '',
            this.selectedCourse='',
            this.selectedTopic = '',
            this.selectedQuestions= [],
            this.topics= [],
            this.questions= []
            console.log('Test created successfully');
            alert("Test created successfully")
            // You can navigate to a different page or show a success message here
          } else {
            // Handle error
            console.error('Error creating test');
          }
        })
        .catch((error) => {
          console.error('Error creating test:', error);
        });
    },
  },
};
</script>