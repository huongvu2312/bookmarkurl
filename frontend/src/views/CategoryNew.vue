<template>
    <TabSystem v-bind:isActive="'category'" />
    <div class="tab-contents">
        <div class="level">
            <div class="level-left">
                <div class="level-item">
                    <h1 class="title">Add new category</h1>
                </div>
            </div>

            <div class="level-right">
                <div class="level-item">
                    <router-link to="/category" class="button bg-theme1">Back to category list</router-link>
                </div>
            </div>
        </div>

        <form @submit.prevent="submitForm">
            <div class="field">
                <label>Name</label>
                <div class="control">
                    <input type="text" class="input" v-model="name">
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
            name: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Add new bookmark | Bookmark URL'
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.name === '') {
                this.errors.push('The name is missing')
            }
            if (!this.errors.length) {
                const formData = {
                    name: this.name
                }
                axios
                    .post("/api/v1/categorys/", formData)
                    .then(response => {
                        toast({
                            message: 'Category created!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/' + response.data.get_absolute_url)
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
