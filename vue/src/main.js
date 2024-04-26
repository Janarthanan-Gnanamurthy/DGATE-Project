import 'animate.css'
import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import keycloak from './keycloak'

const app = createApp(App)

// Initialize Keycloak
keycloak.init({ onLoad: 'check-sso' }).then(authenticated => {
  if (authenticated) {
    // Configure Vue Router with Keycloak
    router.beforeEach((to, from, next) => {
      if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!keycloak.authenticated || !keycloak.token) { // Check for both authentication and token
          // Redirect to custom login page (replace with your component path)
          next('/login');
        } else {
          next();
        }
      } else {
        next();
      }
    });


    app.use(router)
    app.use(store)
    app.mount('#app')
  } else {
    console.error('Failed to authenticate with Keycloak')
  }
}).catch(error => {
  console.error('Failed to initialize Keycloak', error)
})

