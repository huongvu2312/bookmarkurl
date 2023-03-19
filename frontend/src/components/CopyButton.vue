
<template>
    <button type="button" @click="copyUrl(bookmarkId)" class="button is-info fas fa-copy"></button>
</template>

<script>
import axios from 'axios'

export default {
    name: 'CopyButton',
    props: {
        bookmarkId: 0,
    },
    methods: {
        async copyUrl(bookmarkId) {
            await axios
                .put("/api/v1/add-copy-bookmark/" + bookmarkId + "/")
                .then(response => {
                    navigator.clipboard.writeText(response.data.url);
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
    }
}
</script>