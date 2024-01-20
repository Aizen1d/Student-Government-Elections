<template>
    <title>Rules & Guidelines - COMELEC Portal</title>
    <Navbar></Navbar>

    <main class="main-margin">
        <h1 class="header">RULES</h1>

        <div class="rule-list" v-if="isRuleSucess" v-for="(rule, index) in rulesData.rules" :key="index">
            <div class="rule">
                <div class="rule-wrapper">
                    <span class="rule-title">Rule {{ rule.count }} {{ rule.RuleTitle }}</span>

                    <hr class="line">

                    <p class="rule-content">{{ rule.RuleBody }}</p>
                </div>
            </div>
        </div>

        <hr class="divider">

        <h1 class="header">GUIDELINES</h1>

        <div class="rule-list" v-if="isGuidelineSucess" v-for="(guideline, index) in guidelinesData.guidelines" :key="index">
            <div class="rule">
                <div class="rule-wrapper">
                    <span class="rule-title">Guideline {{ guideline.count }} {{ guideline.GuidelineTitle }}</span>

                    <hr class="line">

                    <p class="rule-content">{{ guideline.GuidelineBody }}</p>
                </div>
            </div>
        </div>
    </main>

    <Appeal></Appeal>
</template>

<script>
    import Navbar from "../Shared/Navbar.vue";
    import Standards from "../Shared/Standards.vue";
    import Appeal from "../Shared/Appeal.vue";

    import { useQuery } from "@tanstack/vue-query";
    import { ref } from "vue";
    import axios from "axios";

    export default {
        setup() {
            const fetchRules = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/rule/all`);
                return response.data;
            };

            const fetchGuidelines = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/guideline/all`);
                return response.data;
            };

            const page = ref(1);
            const { data: rulesData, 
                    isLoading: isRuleLoading, 
                    isSuccess: isRuleSucess,
                    isError: isRuleError,
                    isStale: isRuleStale, } = 
                    useQuery({
                        queryKey: ["rules"],
                        queryFn: fetchRules,
                    });

            const { data: guidelinesData, 
                    isLoading: isGuidelineLoading, 
                    isSuccess: isGuidelineSucess, 
                    isError: isGuidelineError, } = 
                    useQuery({
                        queryKey: ["guidelines"],
                        queryFn: fetchGuidelines,
                    });
                    
            return { 
                rulesData,
                isRuleLoading,
                isRuleSucess,
                isRuleError,
                guidelinesData,
                isGuidelineLoading,
                isGuidelineSucess,
                isGuidelineError,
            };
        },
        components: {
            Navbar,
            Standards,
            Appeal,
        },
    };
</script>

<style scoped>
.main-margin{
    margin: 0% 8%;
}

.header{
    margin: 1.5% 0%;
    font-size: 28px;
    font-weight: bold;
}

.rule{
    background-color: #ffffff;
    box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
    border-radius: 6px;
    margin: 1.5% 0%;
}

.rule-wrapper{
    padding: 2%;
}

.rule-title{
    font-weight: bold;
    font-size: 20px;
    margin: 0%;
}

.line{
    border: 0;
    height: 2px;
    background: rgb(249,249,249);
    background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
    margin: 1% 0%;
}

.divider{
    border: 0;
    height: 2px;
    background: rgb(249,249,249);
    background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
    margin: 3% 0%;
}


.rule-content{
    margin: 0%;
    font-size: 18px;
    text-indent: 70px;
}
</style>