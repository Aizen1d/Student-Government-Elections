<template>
    <Navbar></Navbar>

    <div class="container-fluid main">
        <div class="sector mx-5">
            <h1 class="my-4 rules-label">RULES</h1>
            
            <div class="details" v-if="isRuleSucess" v-for="(rule, index) in rulesData.rules" :key="index">
                <span>Rule #{{ rule.count }} {{ rule.RuleTitle }}</span>
                <p class="my-2">{{ rule.RuleBody }}</p>
            </div>
        </div>

        <div class="sector mx-5">
            <h1 class="my-4 guidelines-label">GUIDELINES</h1>

            <div class="details" v-if="isGuidelineSucess" v-for="(guideline, index) in guidelinesData.guidelines" :key="index">
                <span>Guideline #{{ guideline.count }} {{ guideline.GuidelineTitle }}</span>
                <p class="my-2">{{ guideline.GuidelineBody }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import Navbar from "../Shared/Navbar.vue";
    import Standards from "../Shared/Standards.vue";

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
        },
    };
</script>

<style scoped>
.main {
    font-size: 20px;
    margin-top: 3%;
}

.main h1 {
    font-size: 20px;
    letter-spacing: 3px;
    font-weight: 800;
}

.sector {
    margin: 3% 0 3% 0;
}

.rules-label {
    font-size: 1.5em !important;
    letter-spacing: 0.2em !important;
}

.guidelines-label {
    font-size: 1.5em !important;
    letter-spacing: 0.2em !important;
}

.details {
    margin-top: 2%;
}

.details span {
    font-weight: 700;
}
</style>