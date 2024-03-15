import Keycloak from 'keycloak-js'

// Configure Keycloak instance
const keycloak = new Keycloak({
  url: 'http://localhost:8080/',
  realm: 'Myrealm',
  clientId: 'myclient'
})

export default keycloak