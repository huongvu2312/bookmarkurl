<template>
    <TabSystem v-bind:isActive="'bookmark'" />
    <div class="tab-contents">
        <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <h1 class="title">Add new bookmark</h1>
                </div>
            </div>

            <div class="level-right">
                <div class="level-item">
                    <router-link to="/bookmark" class="button bg-theme1">Back to bookmark list</router-link>
                </div>
            </div>
        </div>

        <form @submit.prevent="submitForm">
            <div class="field">
                <label>URL</label>
                <div class="control">
                    <input type="text" class="input" v-model="url">
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

            <div class="notification is-danger" v-if="errors.length">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>

            <div class="field">
                <div class="control">
                    <button class="button bg-theme1">Add</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'

export default {
    name: 'BookmarkNew',
    components: {
        TabSystem
    },
    data() {
        return {
            url: '',
            category: '',
            note: '',
            options: [],
            errors: []
        }
    },
    mounted() {
        document.title = 'Add new bookmark | Bookmark URL'
        this.getCategory()
    },
    methods: {
        async getCategory() {
            await axios
                .get(`/api/v1/categorys/`)
                .then(response => {
                    this.options = response.data

                    const category_slug = this.$route.query.to
                    if (category_slug) {
                        axios
                            .get(`/api/v1/categorys/${category_slug}/`)
                            .then(response => {
                                this.category = response.data.id
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
                    } else this.category = this.options[0].id
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
                    url: this.url,
                    category: this.category,
                    note: this.note
                }
                axios
                    .post("/api/v1/bookmarks/", formData)
                    .then(response => {
                        toast({
                            message: 'Bookmark created!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })

                        let toPath = '/bookmark'
                        if (this.$route.query.to) toPath = '/category/' + this.$route.query.to
                        this.$router.push(toPath)
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
        }
    },
}
</script>
