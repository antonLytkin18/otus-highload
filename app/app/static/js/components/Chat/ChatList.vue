<template>
    <div>
        <v-select
                :options="followerList"
                :reduce="user => user.id"
                placeholder="Start messaging with..."
                @input="setSelected"
        >
            <template slot="option" slot-scope="option">
                <b-avatar
                        button
                        variant="secondary"
                        :size="20"
                        class="align-center"
                ></b-avatar> {{ option['last_name'] }} {{option['name']}}
            </template>
            <template slot="selected-option" slot-scope="option">
                {{ option['last_name'] }} {{option['name']}}
            </template>
        </v-select>
        <hr>
        <b-list-group v-if="!!chatList.length">
            <b-list-group-item
                v-for="(item, index) in chatList"
                :href="populateUrl(chatMessageListUrl, {id: item['user_id']})"
                class="flex-column align-items-start"
            >
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ item['user_name'] }}</h5>
                    <small
                        v-if="item['last_message']"
                    >
                      {{ item['last_message']['date_create'] }}
                    </small>
                </div>

                <b-badge
                        v-if="item['unread_messages_count']"
                        class="float-right"
                        variant="danger"
                >{{ item['unread_messages_count'] }}</b-badge>

                <p
                    v-if="item['last_message']"
                    class="mb-1 text-muted"
                >
                    Last message: {{ item['last_message']['message'] }}
                </p>
                <p
                    v-else
                    class="mb-1 text-muted"
                >
                    There are no messages posted yet
                </p>
            </b-list-group-item>
        </b-list-group>
        <b-alert v-else show variant="info">There are no chats. Start messaging with somebody</b-alert>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.makeChatAppRequest('get', '/api/v1/chats')
                .then(response => {
                    const {data} = response;
                    this.chatList = data['list'];
                });
        },
        props: {
            followerList: Object | Array,
            chatMessageListUrl: String,
        },
        data: () => ({
            chatList: {},
        }),
        methods: {
            setSelected: function (userId) {
                window.open(this.populateUrl(this.chatMessageListUrl, {id: userId}), '_self');

            }
        },
    }
</script>

<style scoped>

</style>