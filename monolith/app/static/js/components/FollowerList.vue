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
                        >{{ item['name'] }}
                        </b-link>
                        <div>Age: {{ item['age'] }}</div>
                        <div>City: {{ item['city'] }}</div>
                    </b-col>
                </b-row>
            </b-card-body>
            <template v-slot:footer>
                <v-follower-actions
                        :item="item"
                        :send-url="sendUrl"
                        :accept-url="acceptUrl"
                        @accepted="onAccept($event, item)"
                        @sent="onSend($event, item)"
                ></v-follower-actions>
            </template>
        </b-card>
    </div>
</template>

<script>
    export default {
        props: {
            list: Object | Array,
            followerUrl: String,
            sendUrl: String,
            acceptUrl: String,
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
        }
    }
</script>

<style scoped>
    .follower-link {
        color: rgba(0, 0, 0, 0.5);
        font-weight: bold;
        font-size: 18px;
    }
</style>