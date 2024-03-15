import 'animate.css'
import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import keycloak from './keycloak'

const app = createApp(App)

// Initialize Keycloak
keycloak.init({ onLoad: 'login-required' }).then(authenticated => {
  if (authenticated) {
    // Configure Vue Router with Keycloak
    router.beforeEach((to, from, next) => {
      if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!keycloak.authenticated) {
          next('/');
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

