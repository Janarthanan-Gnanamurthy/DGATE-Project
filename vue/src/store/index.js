import { createStore } from 'vuex'

const store = createStore({
	state(){
		return {
			user: {id: 1, name: 'Balaji', email:'janagnana12@gmail.com', password:'123456', department:'MECH'},
			courseId: null,
			courses: null,
			course: null,
			topic: null,
			test: null,
			test_result:null,
			results: null,
		}
	},
	mutations: {
		getUser(state, user){
			state.user = user
		},
		getCourseId(state, courseId){
			state.courseId = courseId
		},
    getCourses(state, courses) {
      state.courses = courses
      // Save the courses to localStorage
      localStorage.setItem('appData', JSON.stringify(state));
    },
    getCourse(state, course) {
      state.course = course
      // Save the course to localStorage
      localStorage.setItem('appData', JSON.stringify(state));
    },
		getTopic(state, topic){
			state.topic = topic
			localStorage.setItem('appData', JSON.stringify(state));
		},
		getTest(state, test){
			state.test = test;
      localStorage.setItem('appData', JSON.stringify(state));
		},
		deleteTest(state){
			state.test = null
      localStorage.setItem('appData', JSON.stringify(state));
		},
		getResults(state, results){
			state.results = results
			localStorage.setItem('appData', JSON.stringify(state));
		},
		getTestResult(state, test_result){
			state.test_result=test_result
			localStorage.setItem('appData', JSON.stringify(state))
		}
	},
	actions: {
		async getCourses({ commit }) {
			try {
				const response = await fetch(`http://localhost:8000/courses`);

				if (!response.ok) {
						throw new Error(`HTTP error! Status: ${response.status}`);
				}

				const data = await response.json();
				console.log('Courses Fetched', data);
				commit('getCourses', data);
			} catch (error) {
				console.error('Error fetching courses:', error);
				alert('Error fetching courses. Please try again.');
			}
		},
		async getCourse({ commit }, course_id) {
			try {
				const response = await fetch(`http://localhost:8000/course/${course_id}`);

				if (!response.ok) {
						throw new Error(`HTTP error! Status: ${response.status}`);
				}

				const data = await response.json();
				console.log('Course Fetched', data);
				commit('getCourse', data);
				return data

			} catch (error) {
				console.error('Error fetching course:', error);
				alert('Error fetching course. Please try again.');
			}
		},
		async getTest({ commit }, test_id) {
			try {
				const response = await fetch(`http://localhost:8000/test/${test_id}`);
				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`);
				}
		
				const data = await response.json();
				console.log('Test Fetched', data);
		
				// Assuming 'getTest' mutation updates the 'test' state
				commit('getTest', data);
		
				// Return the data to be used in the component
				return data;
			} catch (error) {
				console.error('Error fetching test:', error);
				alert('Error fetching Test. Please try again.');
				// Propagate the error to the component
				throw error;
			}
		},
		async getTestResult({ commit}, result_id){
			try{
				const response = await fetch(`http://localhost:8000/result/${result_id}`)
				if (!response.ok){
					throw new Error(`HTTP error! Status: ${response.status}`)
				}

				const data = await response.json();
				console.log('TestResult Fetched', data);

				commit('getTestResult', data);

			}catch (error) {
				console.error('Error fetching courses:', error);
				alert('Error fetching User. Please try again.');
			}
		},			
		async getResults(context){
			try{
				const response = await fetch(`http://localhost:8000/results/${context.state.user.id}`)
				if (!response.ok){
					throw new Error(`HTTP error! Status: ${response.status}`)
				}

				const data = await response.json();
				console.log('Results Fetched', data);

				context.commit('getResults', data);

			}catch (error) {
				console.error('Error fetching courses:', error);
				alert('Error fetching User. Please try again.');
			}
		},
		initStore({ commit }) {
			const storedData = localStorage.getItem('appData');
			console.log(storedData)
			if (storedData) {
				const { courses, course, topic, test, test_result, results } = JSON.parse(storedData);

				if (courses) {
					commit('getCourses', courses);
				}
		
				if (course) {
					commit('getCourse', course);
				}
				
				if (topic) {
					commit('getTopic', topic);
				}

				if (test) {
					commit('getTest', test);
				}

				if (test_result) {
					commit('getTestResult', test_result);
				}

				if (results) {
					commit('getResults', results);
				}
			}
		},
	}
})


// Initialize the store when your application starts
store.dispatch('initStore')

export default store