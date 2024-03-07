<template>
  <main>
    <input type="number" v-model="topic_id">
    <input class="p-5 text-2xl" type="file" @change="handleFileUpload" accept=".xlsx" />
  </main>
</template>

<script>
  import * as XLSX from 'xlsx';

  export default {
    data(){
      return {
        topic_id: null
      }
    },
    methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = () => {
        const data = new Uint8Array(reader.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[2]];
        let jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
        jsonData = jsonData.slice(3);
        console.log(jsonData)

        // Send jsonData to the backend
        this.sendDataToBackend(jsonData);
      };

      reader.readAsArrayBuffer(file);
    },

    sendDataToBackend(jsonData) {
      // Here, you can use an HTTP client library (e.g., axios) to send the data to your backend
      // Replace the following code with the appropriate method for your backend
      fetch(`http://localhost:8000/upload/${this.topic_id}`, {
        method: 'POST',
        body: JSON.stringify(jsonData),
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