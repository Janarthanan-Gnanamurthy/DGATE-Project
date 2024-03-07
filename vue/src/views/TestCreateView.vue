<template>
  <div class="container mx-auto p-10">
    <h2 class="text-3xl font-semibold mb-6">Create Test</h2>
 
    <div class="mb-6">
      <label for="testNameInput" class="block text-xl font-semibold mb-2">Enter a Name for the Test:</label>
      <input
        id="testNameInput"
        type="text"
        v-model="testName"
        placeholder="Enter Test name"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </div>
 
    <div class="mb-6">
      <label for="course-select" class="block text-xl font-semibold mb-2">Select Course:</label>
      <select
        id="course-select"
        v-model="selectedCourse"
        @change="fetchTopics"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="">Select Course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.title }}</option>
      </select>
    </div>
 
    <div v-if="topics.length > 0" class="mb-6">
      <label for="topic-select" class="block text-xl font-semibold mb-2">Select Topic:</label>
      <select
        id="topic-select"
        v-model="selectedTopic"
        @change="fetchQuestions"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="">Select Topic</option>
        <option v-for="topic in topics" :key="topic.id" :value="topic.id">{{ topic.title }}</option>
      </select>
    </div>
 
    <div v-if="questions.length > 0" class="overflow-auto" style="max-height: 400px;">
      <table class="w-full table-auto">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2 w-16">Select</th>
            <th class="px-4 py-2 w-16">Q.ID</th>
            <th class="px-4 py-2">Question</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id" class="odd:bg-gray-100">
            <td class="px-4 py-2">
              <input type="checkbox" v-model="selectedQuestions" :value="question.id" class="form-checkbox" />
            </td>
            <td class="px-4 py-2">{{ question.id }}</td>
            <td class="px-4 py-2">{{ question.statement }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button
        @click="createTest"
        class="btn btn-primary px-6 py-3 rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 mt-4"
      >
        Create Test
    </button>
  </div>
 </template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'CreateTest',
  data() {
    return {
      testName: null,
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
      if (!this.testName){
        alert('Please Enter Test Name. ')
      }
      else {
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
      }
    },
  },
};
</script>