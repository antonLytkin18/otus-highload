<template>
    <div>
        <b-card v-for="(item, index) in list"
                style="margin-bottom: 5px"
                no-body
        >
            <b-card-body class="small text-muted">
                <b-row>
                    <b-col cols="1">
                        <b-avatar
                                button
                                variant="secondary"
                                :size="60"
                                class="align-center"
                                @click="onProfileClick($event, item['id'])"
                        ></b-avatar>
                    </b-col>
                    <b-col cols="11">
                        <b-link
                                class="follower-link"
                                @click="onProfileClick($event, item['id'])"
                        >{{item['last_name']}} {{ item['name'] }}
                        </b-link>
                        <div>Birth Date: {{ item['birth_date'] }}</div>
                        <div>City: {{ item['city'] }}</div>
                    </b-col>
                </b-row>
            </b-card-body>
            <template v-if="showActions" v-slot:footer>
                <v-follower-actions
                        :item="item"
                        :send-url="sendUrl"
                        :accept-url="acceptUrl"
                        @accepted="onAccept($event, item)"
                        @sent="onSend($event, item)"
                ></v-follower-actions>
            </template>
        </b-card>
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
            list: Object | Array,
            followerUrl: String,
            followersUrl: String,
            sendUrl: String,
            acceptUrl: String,
            pagination: Object,
            showActions: {
                type: Boolean,
                default: true
            },
        },
        methods: {
            onSend: function (e, item) {
                item['is_sent'] = true;
            },
            onAccept: function (e, item) {
                item['is_friend'] = true;
            },
            onProfileClick: function (e, id) {
                window.open(this.populateUrl(this.followerUrl, {id: id}), '_blank');
            },
            onPageChange: function (page) {
                window.open(this.populateUrl(this.followersUrl, {page: page}), '_self');
            }
        }
    }
</script>

<style scoped>
    .follower-link {
        color: rgba(0, 0, 0, 0.5);
        font-weight: bold;
        font-size: 18px;
    }

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