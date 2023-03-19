<template>
  <TabSystem v-bind:isActive="'myaccount'" />
  <div class="tab-contents">
    <div class="tab-contents">
      <div class="level">
        <div class="level-left">
          <div class="level-item">
            <h1 class="title">My account</h1>
          </div>
        </div>
        <div class="level-right">
          <div class="level-item">
            <router-link to="/my-account/change-password" class="button bg-theme1">Change password</router-link>
          </div>
        </div>
      </div>

      <form @submit.prevent="submitForm">
        <div class="field">
          <label>Username</label>
          <div class="control">
            <input type="text" class="input" v-model="username">
          </div>
        </div>

        <div class="field">
          <label>Email</label>
          <div class="control">
            <input type="text" class="input" v-model="email">
          </div>
        </div>

        <div class="notification is-danger" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>

        <div class="field">
          <div class="control">
            <button class="button bg-theme1">Update</button>
          </div>
        </div>
      </form>

      <br>
      <p>
        You had in total <b>{{ totalBookmarks }}</b> bookmark(s), in which <b>{{ totalNoCategoryBookmarks }}</b>
        bookmark(s) have no category and <b>{{ totalRestBookmarks }}</b> bookmark(s) belong to <b>{{ totalCategorys }}</b>
        categories.
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'

export default {
  name: 'MyAccountView',
  components: {
    TabSystem
  },
  data() {
    return {
      user: {
        bookmarks: [],
        categorys: []
      },
      username: '',
      email: '',
      errors: []
    }
  },
  mounted() {
    document.title = 'My Account | Bookmark URL'
    this.getUser()
  },
  methods: {
    async getUser() {
      await axios
        .get("/api/v1/user/")
        .then(response => {
          this.user = response.data
          this.username = response.data.username
          this.email = response.data.email
        })
        .catch(error => {
          console.log(error)
        })
    },
    submitForm() {
      this.errors = []
      if (this.username === '') {
        this.errors.push('The username is missing')
      }
      if (this.email === '') {
        this.errors.push('The email is missing')
      }
      if (!this.errors.length) {
        const formData = {
          username: this.username,
          email: this.email,
        }

        axios
          .put("/api/v1/user/", formData)
          .then(response => {
            toast({
              message: 'User updated!',
              type: 'is-success',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'bottom-right',
            })
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }

              console.log(JSON.stringify(error.response.data))
            } else if (error.message) {
              this.errors.push('Something went wrong. Please try again')

              console.log(JSON.stringify(error))
            }
          })
      }
    },
  },
  computed: {
    totalBookmarks() {
      return this.user.bookmarks.length
    },
    totalNoCategoryBookmarks() {
      const noCategory = this.user.categorys.filter(i => i.slug === 'no-category')
      if (noCategory.length) return noCategory[0].bookmarks.length
      return 0
    },
    totalCategorys() {
      return this.user.categorys.length - 1
    },
    totalRestBookmarks() {
      return this.totalBookmarks - this.totalNoCategoryBookmarks
    }
  }
}
</script>
