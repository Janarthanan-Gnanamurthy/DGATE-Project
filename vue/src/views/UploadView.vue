<template>
  <main class="container mx-auto p-10">
    <div class="mb-6">
      <label for="course-select" class="block text-2xl font-semibold mb-2">Select Course:</label>
      <select
        id="course-select"
        v-model="selectedCourse"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        @change="showAddCourseModal"
      >
        <option value="">Select Course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.title }}</option>
        <option value="-1">Add New Course</option>
      </select>
    </div>

    <div>
      <!-- The modal -->
      <div v-if="showModal" class="modal modal-open">
        <div class="modal-box relative">
          <div class="text-3xl font-extrabold pb-7">Add New Course</div>
          <label for="course-title" class="block text-xl font-semibold mb-2">Course Title:</label>
          <input
            id="course-title"
            type="text"
            v-model="newCourseTitle"
            class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
          />

          <label for="course-code" class="block text-xl font-semibold mb-2">Course Code:</label>
          <input
            id="course-code"
            type="text"
            v-model="newCourseCode"
            class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
          />

          <div class="modal-action">
            <button @click="addNewCourse" class="btn btn-primary">Add</button>
            <button @click="closeModal" class="btn btn-ghost">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-6">
      <label for="fileInput" class="block text-2xl font-semibold mb-2">Upload Excel File:</label>
      <input
        id="fileInput"
        type="file"
        @change="handleFileUpload"
        accept=".xlsx"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </div>

    <div class="mb-6">
      <label for="sheetDropdown" class="block text-2xl font-semibold mb-2">Select Topic:</label>
      <select
        id="sheetDropdown"
        v-model="selectedSheet"
        @change="sheetToJson"
        class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="">Select Sheet</option>
        <option v-for="sheet in sheetNames" :key="sheet" :value="sheet">{{ sheet }}</option>
      </select>
    </div>

    <button
      @click="createTopic"
      class="btn btn-primary px-6 py-3 rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
      Upload
    </button>
  </main>
</template>

<script>
import { mapState } from 'vuex';
  import * as XLSX from 'xlsx';

  export default {
    data(){
      return {
        topic_id: null,
        showModal: false,
        selectedSheet: '',
        selectedCourse: '',
        newCourseTitle: '',
        newCourseCode:'',
        sheetNames: [],
        workbook: null,
        jsonData: null
      }
    },
    computed: {
    ...mapState(['courses']),
    },
    async created() {
      await this.$store.dispatch('getCourses');
    },
    methods: {
      handleFileUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = () => {
          const data = new Uint8Array(reader.result);
          this.workbook = XLSX.read(data, { type: 'array' });

          // Update sheetNames to contain all sheet names
          this.sheetNames = this.workbook.SheetNames;
        };

        reader.readAsArrayBuffer(file);
      },
      sheetToJson(){
          const worksheet = this.workbook.Sheets[this.selectedSheet];
          this.jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
          this.jsonData = this.jsonData.slice(3);
          console.log(this.jsonData);

      },
      async createTopic(){
        const topic_data = {title: this.selectedSheet, course_id: this.selectedCourse}
        try{
          const response = await fetch(`http://localhost:8000/topics`, {
          method: 'POST',
          body: JSON.stringify(topic_data),
          headers: {
            'Content-Type': 'application/json'
          }
        })
          if (!response.ok){
            throw new Error(`HTTP error! Status: ${response.status}`)
          }
          const data = await response.json();
          this.topic_id = data.id

          this.sendDataToBackend()

        }catch (error) {
          console.error('Error fetching courses:', error);
          alert('Error fetching User. Please try again.');
        }
      },
      sendDataToBackend() {
        // Here, you can use an HTTP client library (e.g., axios) to send the data to your backend
        // Replace the following code with the appropriate method for your backend
        fetch(`http://localhost:8000/upload/${this.topic_id}`, {
          method: 'POST',
          body: JSON.stringify(this.jsonData),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          // Handle the response from the backend
          if (response.ok){
            console.log('Sucessfully uploaded questions');
          };
        })
        .catch(error => {
          console.error(error);
        });
      },
      async addNewCourse(){
        const Course = {title:this.newCourseTitle , code: this.newCourseCode}
        try{
          const response = await fetch(`http://localhost:8000/course`, {
          method: 'POST',
          body: JSON.stringify(Course),
          headers: {
            'Content-Type': 'application/json'
          }
        })
          if (!response.ok){
            throw new Error(`HTTP error! Status: ${response.status}`)
          }
          await this.$store.dispatch('getCourses');
          const data = await response.json();
          this.selectedCourse = data.id
          alert('Course Added successfully')
          this.closeModal()

        }catch (error) {
          console.error('Error fetching courses:', error);
          alert('Error fetching User. Please try again.');
        }
      },
      showAddCourseModal(event) {
        if (event.target.value === '-1') {
          this.showModal = true;
        }
      },
      closeModal() {
        this.showModal = false;
        this.newCourseTitle = '';
        this.newCourseCode = '';
      },
    }
  }
</script>