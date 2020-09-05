<template>
    <div>
        <b-input-group class="mt-3">
            <b-form-input
                    v-model="post"
                    @keyup.enter="onPostAdd"
            ></b-form-input>
            <b-input-group-append>
                <b-button
                        variant="outline-success"
                        @click="onPostAdd"
                >
                    Add post
                </b-button>
            </b-input-group-append>
        </b-input-group>
        <hr>
        <b-alert v-if="!listItems.length" show variant="info">There are no news. Add post to be the first</b-alert>
        <v-feed-post
                v-for="(item, index) in listItems"
                :item="item['post']"
                follower-url="/"
        ></v-feed-post>
        <b-pagination
                v-if="pagination"
                v-model="pagination['page']"
                :total-rows="pagination['count']"
                :per-page="pagination['per_page']"
                class="pagination-container"
                @change="onPageChange"
        ></b-pagination>
    </div>
</template>

<script>
export default {
    props: {
        userId: String,
        list: Object | Array,
        feedUrl: String,
        addPostUrl: String,
        pagination: Object,
    },
    mounted: function () {
        this.listItems = this.list;
    },
    data: () => ({
        post: '',
        listItems: [],
    }),
    sockets: {
        connect: function () {
            this.$socket.emit('join', {room: 'room_' + this.userId});
        },
        feedUpdated: function (data) {
            axios
                .get(this.populateUrl(this.feedUrl, {page: 1}), {
                    params: {
                        json: true,
                    }
                })
                .then(response => {
                    const {data} = response;
                    this.listItems = data['list'];
                    this.pagination = data['pagination'];
                });
        }
    },
    methods: {
        onPageChange: function (page) {
            window.open(this.populateUrl(this.feedUrl, {page: page}), '_self');
        },
        onPostAdd: function () {
            if (!this.post) {
                return;
            }
            axios
                .post(this.addPostUrl, {
                    message: this.post,
                })
                .then(response => {
                    const {data} = response;
                    if (!data['success']) {
                        this.$emit('error', data);
                        return;
                    }
                    const {message} = data;
                    if (!message) {
                        return;
                    }
                    this.listItems.unshift({
                        'post': message
                    })
                    this.$emit('sent', message);

                })
                .finally(() => {
                    this.post = '';
                })
        }
    },
}
</script>

<style scoped>
.pagination-container {
    margin-top: 20px;
}

.pagination-container /deep/ > .page-item .page-link {
    color: #6c757d;
}

.pagination-container /deep/ > .page-item.active .page-link {
    background-color: rgba(0, 0, 0, 0.5);
    border-color: #ffffff;
    color: #ffffff;
}
</style>