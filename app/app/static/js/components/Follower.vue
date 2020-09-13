<template>
    <b-card
            style="margin-bottom: 5px"
            no-body
    >
        <b-tabs card>
            <b-tab title="Profile" active>
                <b-card-body class="small text-muted">
                    <b-row>
                        <b-col cols="1">
                            <b-avatar
                                    variant="secondary"
                                    :size="60"
                                    class="align-center"
                            ></b-avatar>
                        </b-col>
                        <b-col cols="11">
                            {{ item['name'] }}
                            <div>Birth Date: {{ item['birth_date'] }}</div>
                            <div>City: {{ item['city'] }}</div>
                        </b-col>
                    </b-row>
                </b-card-body>
            </b-tab>
            <b-tab title="Followers" v-bind:disabled="!followers.length">
                <b-list-group>
                    <b-list-group-item
                            v-for="(follower, index) in followers"
                            :href="populateUrl(followerUrl, {id: follower['id']})"
                            target="_blank"
                    >
                        <b-avatar
                                variant="secondary"
                                class="align-center"
                        ></b-avatar>
                        {{ follower['name'] }}
                    </b-list-group-item>
                </b-list-group>
            </b-tab>
        </b-tabs>
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
</template>

<script>
    export default {
        props: {
            item: Object,
            followers: Array | Object,
            followerUrl: String,
            sendUrl: String,
            acceptUrl: String,
        },
        data: () => ({
            buttonsPressed: [],
        }),
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

</style>