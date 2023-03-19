<template>
    <TabSystem v-bind:isActive="'category'" />
    <div class="tab-contents">
        <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <router-link to="/category" class="button bg-theme1">Back to category list</router-link>
                </div>
            </div>
            <div class="level-right">
                <div class="level-item">
                    <router-link :to="{ path: '/bookmark/new', query: { to: $route.params.category_slug } }"
                        class="button bg-theme1">Add new bookmark</router-link>
                </div>
                <div class="level-item">
                    <button @click="deleteCategory()" class="button is-danger">Delete this category</button>
                </div>
            </div>
        </div>

        <form @submit.prevent="submitForm">
            <label>Name</label>
            <div class="field has-addons">
                <div class="control is-expanded">
                    <input type="text" class="input" v-model="name">
                </div>
                <div class="control">
                    <button class="button bg-theme1">Update</button>
                </div>
            </div>

            <div class="notification is-danger" v-if="errors.length">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
        </form>
        <br>
        <table class="table" v-if="bookmarks.length">
            <tbody>
                <tr v-for="(bookmark, key) in bookmarks">
                    <td>
                        <router-link :to="'/' + bookmark.get_absolute_url" class="button bg-theme1">{{ key + 1
                        }}</router-link>
                    </td>
                    <td>
                        {{ bookmark.url }}&nbsp;&nbsp;&nbsp;
                        <CopyButton v-bind:bookmarkId="bookmark.id"></CopyButton>
                    </td>
                    <td>{{ bookmark.category.name }}</td>
                    <td>{{ bookmark.created_at }}</td>
                    <td>{{ bookmark.note }}</td>
                    <td><button @click="deleteBookmark(bookmark.id)" class="button fas fa-trash is-danger"></button></td>
                    <td v-if="$route.params.category_slug != 'no-category'">
                        <button @click="removeBookmark(bookmark.id)" class="button is-warning">Remove from category</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-else>There is no bookmark in this category.</p>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'
import CopyButton from '@/components/CopyButton.vue'

export default {
    name: 'BookmarkDetail',
    components: {
        TabSystem,
        CopyButton
    },
    data() {
        return {
            name: '',
            bookmarks: [],
            errors: []
        }
    },
    mounted() {
        this.getCategory()
    },
    methods: {
        async getCategory() {
            const category_slug = this.$route.params.category_slug
            await axios
                .get(`/api/v1/categorys/${category_slug}/`)
                .then(response => {
                    this.name = response.data.name
                    this.bookmarks = response.data.bookmarks
                    document.title = response.data.name + ' | Bookmark URL'
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
        },
        submitForm() {
            this.errors = []
            if (this.name === '') {
                this.errors.push('The name is missing')
            }
            if (!this.errors.length) {
                const formData = {
                    name: this.name
                }
                const category_slug = this.$route.params.category_slug

                axios
                    .put(`/api/v1/categorys/${category_slug}/`, formData)
                    .then(response => {
                        toast({
                            message: 'Category updated!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/' + response.data.data.get_absolute_url)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        async deleteCategory() {
            if (confirm("This will delete all bookmarks belonged to this category as well. Do you really want to delete?")) {
                const category_slug = this.$route.params.category_slug

                axios
                    .delete(`/api/v1/categorys/${category_slug}/`)
                    .then(response => {
                        toast({
                            message: 'Category deleted!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                        this.$router.push('/category')
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        async deleteBookmark(bookmark_id) {
            if (confirm("Do you really want to delete this bookmark?")) {
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
                        this.bookmarks = this.bookmarks.filter(i => i.id !== bookmark_id)
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        async removeBookmark(bookmark_id) {
            const formData = {
                removeCategory: true,
            }

            axios
                .put(`/api/v1/bookmarks/${bookmark_id}/`, formData)
                .then(response => {
                    toast({
                        message: 'Bookmark removed!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                    this.bookmarks = this.bookmarks.filter(i => i.id !== bookmark_id)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
}
</script>
