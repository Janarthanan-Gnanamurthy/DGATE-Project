<template>
  <main class="p-10">
    <div class="text-2xl">
      <label for="course-select">Select Course:</label>
      <select id="course-select" v-model="selectedCourse">
        <option value="">Select Course</option>
        <option v-for="course in courses" :key="course.id" :value="course.id">{{ course.title}}</option>
      </select>
    </div>
    <input class="my-5 text-2xl" type="file" @change="handleFileUpload" accept=".xlsx" /> <br>
    <label for="sheetDropdown">Select Topic:</label>
    <select id="sheetDropdown" v-model="selectedSheet" @change="sheetToJson">
      <option value="">Select Sheet</option>
      <option v-for="sheet in sheetNames" :key="sheet" :value="sheet">{{ sheet }}</option>
    </select><br>
    <button @click="createTopic" class="btn btn-primary">Upload</button>
  </main>
</template>

<script>
import { mapState } from 'vuex';
  import * as XLSX from 'xlsx';

  export default {
    data(){
      return {
        topic_id: null,
        selectedSheet: null,
        selectedCourse: null,
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

          // Set selectedSheet to the first sheet by default (change as needed)
          this.selectedSheet = this.sheetNames[0];
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
      }
    }
  }
</script>