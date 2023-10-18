<template>
    <Navbar></Navbar>

    <div class="container-fluid main">
        <div class="sector mx-5">
            <h1 class="my-4 rules-label">RULES</h1>

            <div class="details" v-for="(rule, index) in rules" :key="index">
                <span>{{ rule.count }} {{ rule.title }}</span>
                <p class="my-2">{{ rule.body }}</p>
            </div>
        </div>

        <div class="sector mx-5">
            <h1 class="my-4 guidelines-label">GUIDELINES</h1>

            <div class="details" v-for="(guideline, index) in guidelines" :key="index">
                <span>{{ guideline.count }} {{ guideline.title }}</span>
                <p class="my-2">{{ guideline.body }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'

    import axios from 'axios'
    import { ref } from 'vue'

    export default {
        setup() {
            const rules = ref([]);
            const guidelines = ref([]);

            return {
                rules,
                guidelines
            }
        },
        components: {
            Standards,
            Navbar,
        },
        created() {
            this.fetchRules();
            this.fetchGuidelines();
        },
        methods: {
            fetchRules() {
                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/all`)
                    .then(response => {
                    console.log(`Get all rules successful. Duration: ${response.duration}ms`)

                    const rules = response.data.rules.map(rule => ({
                        id: rule.RuleId,
                        count: "Rule #" + rule.count,
                        type: rule.type,
                        title: rule.RuleTitle,
                        body: rule.RuleBody
                    }));

                    this.rules = rules;
                });
            },

            fetchGuidelines() {
                axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/all`)
                    .then(response => {
                    console.log(`Get all guidelines successful. Duration: ${response.duration}ms`)

                    const guidelines = response.data.guidelines.map(guideline => ({
                            id: guideline.GuideId,
                            count: "Guideline #" + guideline.count,
                            type: guideline.type,
                            title: guideline.GuidelineTitle,
                            body: guideline.GuidelineBody
                        }));

                    this.guidelines = guidelines;
                });
            },
        }
    }
</script>

<style scoped>
    .main{
        font-size: 20px;
        margin-top: 3%;
    }

    .main h1{
        font-size: 20px;
        letter-spacing: 3px;
        font-weight: 800;
    }

    .sector{
        margin: 3% 0 3% 0;
    }

    .rules-label{
        font-size: 1.5em !important;
        letter-spacing: 0.2em !important;
    }

    .guidelines-label{
        font-size: 1.5em !important;
        letter-spacing: 0.2em !important;
    }

    .details{
        margin-top: 2%;
    }

    .details span{
        font-weight: 700;
    }
</style>