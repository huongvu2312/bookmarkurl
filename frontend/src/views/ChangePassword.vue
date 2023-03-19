<template>
    <TabSystem v-bind:isActive="'myaccount'" />
    <div class="tab-contents">
        <div class="tab-contents">
            <router-link to="/my-account" class="button bg-theme1">Back to main account</router-link> <br><br>

            <form @submit.prevent="submitForm">
                <div class="field">
                    <label>Old password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="old_password">
                    </div>
                </div>

                <div class="field">
                    <label>New password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="new_password">
                    </div>
                </div>

                <div class="field">
                    <label>Repeat new password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="new_password2">
                    </div>
                </div>

                <div class="notification is-danger" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <div class="field">
                    <div class="control">
                        <button class="button bg-theme1">Save change</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import TabSystem from '@/components/TabSystem.vue'

export default {
    name: 'ChangePassword',
    components: {
        TabSystem
    },
    data() {
        return {
            old_password: '',
            new_password: '',
            new_password2: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Change password | Bookmark URL'
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.old_password === '') {
                this.errors.push('The old password is missing')
            }
            if (this.new_password === '') {
                this.errors.push('The new password is too short')
            }
            if (this.new_password !== this.new_password2) {
                this.errors.push('The new passwords don\'t match')
            }
            if (!this.errors.length) {
                const formData = {
                    old_password: this.old_password,
                    new_password: this.new_password,
                }

                axios
                    .put("/api/v1/user/", formData)
                    .then(response => {
                        toast({
                            message: 'Password updated! Please login again.',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })

                        axios.defaults.headers.common["Authorization"] = ""

                        localStorage.removeItem("token")
                        localStorage.removeItem("userid")

                        this.$store.commit('removeToken')

                        this.$router.push('/')
                    })
                    .catch(error => {
                        if (error.response) {
                            if (error.response.data.length) {
                                for (const property of error.response.data) {
                                    this.errors.push(property)
                                }
                            } else this.errors.push(error.response.data)
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    })
            }
        },
    }
}
</script>
