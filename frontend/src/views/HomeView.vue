<template>
  <TabSystem v-bind:isActive="'home'" />
  <div class="tab-contents">
    <div v-if="newestBookmarks.length">
      <h1 class="title">Newest</h1>
      <table class="table">
        <tbody>
          <tr v-for="(newest, key) in newestBookmarks">
            <td>{{ key + 1 }}</td>
            <td>
              {{ newest.url }}&nbsp;&nbsp;&nbsp;
              <button @click="copyUrl(newest.id)" class="button is-info fas fa-copy"></button>
            </td>
          </tr>
        </tbody>
      </table>
      <h1 class="title">Most used</h1>
      <table class="table">
        <tbody>
          <tr v-for="(used, key) in usedBookmarks">
            <td>{{ key + 1 }}</td>
            <td>
              {{ used.url }}&nbsp;&nbsp;&nbsp;
              <button @click="copyUrl(used.id)" class="button is-info fas fa-copy"></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else>There is no saved bookmark yet.</p>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'

export default {
  name: 'HomeView',
  components: {
    TabSystem
  },
  data() {
    return {
      newestBookmarks: [],
      usedBookmarks: []
    }
  },
  mounted() {
    document.title = 'Homepage | Bookmark URL'
    this.getNewestBookmarks()
    this.getUsedBookmarks()
  },
  methods: {
    async getNewestBookmarks() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get(`/api/v1/newest-bookmarks/`)
        .then(response => {
          this.newestBookmarks = response.data
        })
        .catch(error => {
          console.log(error)
          toast({
            message: 'Something went wrong. Please try again.',
            type: 'is-danger',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'bottom-right',
          })
        })
      this.$store.commit('setIsLoading', false)
    },
    async getUsedBookmarks() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get(`/api/v1/used-bookmarks/`)
        .then(response => {
          this.usedBookmarks = response.data
        })
        .catch(error => {
          console.log(error)
          toast({
            message: 'Something went wrong. Please try again.',
            type: 'is-danger',
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: 'bottom-right',
          })
        })
      this.$store.commit('setIsLoading', false)
    },
    async copyUrl(bookmarkId) {
      this.$store.commit('setIsLoading', true)
      await axios
        .put("/api/v1/add-copy-bookmark/" + bookmarkId + "/")
        .then(response => {
          navigator.clipboard.writeText(response.data.url);
          let updatedBookmarkIndex = this.usedBookmarks.findIndex((obj => obj.id == bookmarkId));
          this.usedBookmarks[updatedBookmarkIndex].copy += 1
          this.usedBookmarks.sort((a, b) => b.copy - a.copy);
        })
        .catch(error => {
          console.log(JSON.stringify(error))
        })
      this.$store.commit('setIsLoading', false)
    },
  }
}
</script>
