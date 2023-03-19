
<template>
    <div class="tabs is-fullwidth">
        <ul>
            <li v-bind:class="{ 'is-active': isActive == 'home' }"><router-link to="/home">Home</router-link></li>
            <li v-bind:class="{ 'is-active': isActive == 'bookmark' }"><router-link to="/bookmark">Bookmark</router-link>
            </li>
            <li v-bind:class="{ 'is-active': isActive == 'category' }"><router-link to="/category">Category</router-link>
            </li>
            <li v-bind:class="{ 'is-active': isActive == 'myaccount' }"><router-link to="/my-account">My
                    account</router-link></li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'TabSystem',
    props: {
        isActive: String
    }
}
</script>