<template>
  <TabSystem v-bind:isActive="'bookmark'" />
  <div class="tab-contents">
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <h1 class="title">Bookmark list</h1>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <router-link to="/bookmark/new" class="button fas fa-plus bg-theme1"></router-link>
        </div>
      </div>
    </div>

    <input type="text" v-model="filter" class="input" placeholder="Search by note"><br><br>

    <table class="table" v-if="filteredRows.length">
      <tbody>
        <tr v-for="(bookmark, key) in filteredRows">
          <td>
            <router-link :to="bookmark.get_absolute_url" class="button bg-theme1">{{ key + 1 }}</router-link>
          </td>
          <td>
            {{ bookmark.url }}&nbsp;&nbsp;&nbsp;
            <CopyButton v-bind:bookmarkId="bookmark.id"></CopyButton>
          </td>
          <td>
            <router-link :to="bookmark.category.get_absolute_url" class="cl-theme2">{{ bookmark.category.name
            }}</router-link>
          </td>
          <td>{{ bookmark.created_at }}</td>
          <td>{{ bookmark.note }}</td>
          <td><button @click="deleteBookmark(bookmark.id)" class="button fas fa-trash is-danger"></button></td>
        </tr>
      </tbody>
    </table>
    <p v-else>There is no bookmark.</p>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'
import CopyButton from '@/components/CopyButton.vue'

export default {
  name: 'BookmarkView',
  components: {
    TabSystem,
    CopyButton
  },
  data() {
    return {
      bookmarkList: [],
      filter: '',
    }
  },
  mounted() {
    document.title = 'Bookmark | Bookmark URL'
    this.getBookmarkList()
  },
  methods: {
    async getBookmarkList() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get(`/api/v1/bookmarks/`)
        .then(response => {
          this.bookmarkList = response.data
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
    async deleteBookmark(bookmark_id) {
      if (confirm("Do you really want to delete?")) {
        axios
          .delete(`/api/v1/bookmarks/${bookmark_id}/`)
          .then(response => {
            toast({
              message: 'Bookmark deleted!',
              type: 'is-success',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'bottom-right',
            })
            this.bookmarkList = this.bookmarkList.filter(i => i.id !== bookmark_id)
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  },
  computed: {
    filteredRows() {
      return this.bookmarkList.filter(row => {
        const url = row.url.toString().toLowerCase();
        const note = row.note.toLowerCase();
        const searchTerm = this.filter.toLowerCase();

        return url.includes(searchTerm) ||
          note.includes(searchTerm);
      });
    }
  }
}
</script>
