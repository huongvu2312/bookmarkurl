<template>
    <TabSystem v-bind:isActive="'bookmark'" />
    <div class="tab-contents">
        <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <router-link to="/bookmark" class="button bg-theme1">Back to bookmark list</router-link>
                    <router-link :to="{ path: '/' + categoryUrl }" class="button bg-theme1">Back to
                        category list</router-link>
                </div>
            </div>
            <div class="level-right">
                <div class="level-item">
                    <button @click="deleteBookmark()" class="button is-danger">Delete this bookmark</button>
                </div>
            </div>
        </div>

        <form @submit.prevent="submitForm">
            <label>URL</label>
            <div class="field has-addons">
                <div class="control is-expanded">
                    <input type="text" class="input" v-model="url">
                </div>
                <div class="control">
                    <CopyButton v-bind:bookmarkId="bookmark.id"></CopyButton>
                </div>
            </div>

            <div class="field">
                <label>Category</label>
                <div class="control">
                    <div class="select">
                        <select v-model="category" class="select">
                            <option v-for="option in options" :value="option.id">{{ option.name }}</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="field">
                <label>Note</label>
                <div class="control">
                    <input type="text" class="input" v-model="note">
                </div>
            </div>

            <div class="level">
                <div class="level-right">
                    <div class="level-item">
                        <b>Date added</b>
                    </div>
                    <div class="level-item">
                        {{ bookmark.created_at }}
                    </div>
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
            bookmark: {},
            categoryUrl: '',
            category: '',
            url: '',
            note: '',
            options: [],
            errors: []
        }
    },
    mounted() {
        this.getBookmark()
        this.getCategory()
    },
    methods: {
        async getBookmark() {
            const bookmark_id = this.$route.params.bookmark_id
            await axios
                .get(`/api/v1/bookmarks/${bookmark_id}/`)
                .then(response => {
                    this.bookmark = response.data
                    this.url = this.bookmark.url
                    this.category = this.bookmark.category.id
                    this.note = this.bookmark.note
                    this.categoryUrl = this.bookmark.category.get_absolute_url
                    document.title = 'Bookmark #' + bookmark_id + ' | Bookmark URL'
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
        async getCategory() {
            await axios
                .get(`/api/v1/categorys/`)
                .then(response => {
                    this.options = response.data
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
            if (this.url === '') {
                this.errors.push('The URL is missing')
            }
            if (this.category === '') {
                this.errors.push('The category is missing')
            }
            if (!this.errors.length) {
                const formData = {
                    removeCategory: true,
                }
                const bookmark_id = this.$route.params.bookmark_id

                axios
                    .put(`/api/v1/bookmarks/${bookmark_id}/`, formData)
                    .then(response => {
                        toast({
                            message: 'Bookmark updated!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        },
        async deleteBookmark() {
            if (confirm("Do you really want to delete?")) {
                const bookmark_id = this.$route.params.bookmark_id

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
                        this.$router.push('/bookmark')
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        }
    },
}
</script>
