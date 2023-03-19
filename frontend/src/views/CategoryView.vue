<template>
  <TabSystem v-bind:isActive="'category'" />
  <div class="tab-contents">
    <div class="level">
      <div class="level-left">
        <div class="level-item">
          <h1 class="title">Category list</h1>
        </div>
      </div>
      <div class="level-right">
        <div class="level-item">
          <router-link to="/category/new" class="button fas fa-plus bg-theme1"></router-link>
        </div>
      </div>
    </div>

    <input type="text" v-model="filter" class="input" placeholder="Search by name"><br><br>

    <table class="table" v-if="filteredRows.length">
      <tbody>
        <tr v-for="(category, key) in filteredRows">
          <td>
            <router-link :to="category.get_absolute_url" class="button bg-theme1">{{ key + 1 }}</router-link>
          </td>
          <td>
            {{ category.name }}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>There is no category.</p>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'

export default {
  name: 'CategoryView',
  components: {
    TabSystem
  },
  data() {
    return {
      categoryList: [],
      filter: '',
    }
  },
  mounted() {
    document.title = 'Category | Bookmark URL'
    this.getCategoryList()
  },
  methods: {
    async getCategoryList() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get(`/api/v1/categorys/`)
        .then(response => {
          this.categoryList = response.data
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
  },
  computed: {
    filteredRows() {
      return this.categoryList.filter(row => {
        const name = row.name.toString().toLowerCase();
        const searchTerm = this.filter.toLowerCase();

        return name.includes(searchTerm);
      });
    }
  },
}
</script>
