<template>
  <div id="wrapper">
    <nav class="navbar bg-theme1" v-if="$store.state.isAuthenticated">
      <div class="navbar-brand is-light">
        <router-link to="/" class="navbar-item"><strong>Bookmark URL</strong></router-link>

        <a aria-label="menu" aria-expanded="false" data-target="navbar-menu" class="navbar-burger"
          @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <div class="navbar-item">
            Welcome, {{ username }}
          </div>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <button @click="logout()" class="button is-danger">Log out</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>

    <footer class="footer">
      <p class="has-text-centered">
        Copyright (c) Vu Thu Huong 2023
      </p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      showMobileMenu: false,
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  data() {
    return {
      username: ''
    }
  },
  mounted() {
    if (this.$store.state.isAuthenticated) {
      this.getUsername()
    }
  },
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("userid")

      this.$store.commit('removeToken')

      this.$router.push('/')
    },
    async getUsername() {
      await axios
        .get('/api/v1/user/')
        .then(response => {
          this.username = response.data.username
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style lang="scss">
@import "../node_modules/bulma";

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

.bg-theme1 {
  background-color: #028090;
  color: #fff !important;
}

.cl-theme2 {
  color: #05668D;
}

.navbar.bg-theme1 .navbar-brand>.navbar-item,
.navbar.bg-theme1 .navbar-menu .navbar-start>.navbar-item {
  color: #fff;
}

.section {
  height: auto;
  min-height: 100vh;
}

.footer {
  padding: 3rem 1.5rem 3rem !important;
}
</style>
