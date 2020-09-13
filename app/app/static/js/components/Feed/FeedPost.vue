<template>
    <b-row>
        <b-col>
            <b-card style="margin-bottom: 5px;"
                    no-body
            >
                <b-card-body
                        class="text-muted"
                >
                    {{ item['data'] }}
                </b-card-body>
                <template v-slot:footer>
                    <div class="text-left">
                        <b-avatar
                                button
                                variant="secondary"
                                :size="20"
                                class="align-center"
                                @click="onProfileClick($event, item['user_id'])"
                        ></b-avatar>
                        <span class="small text-muted">{{ item['user']['last_name'] }} {{ item['user']['name'] }}, {{ item['date_create'] }}</span>
                    </div>
                </template>
            </b-card>
        </b-col>
    </b-row>
</template>

<script>
export default {
    props: {
        item: Object | Array,
        followerUrl: String,
    },
    methods: {
        onProfileClick: function (e, id) {
            window.open(this.populateUrl(this.followerUrl, {id: id}), '_blank');
        }
    }
}
</script>

<style scoped>

</style>