<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="container">
        <h1>Elections</h1>
        <p>Full name: {{ full_name }}</p>
        <p>Organization name: {{ organization_name }}</p>
    </div>
</template>

<script>
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import { useUserStore } from '../../Stores/UserStore';

    export default {
        setup(props) {
            const userStore = useUserStore();
            userStore.user_role = props.user_role;
            userStore.full_name = props.full_name;

            return {}
        },
        components: { Navbar, Sidebar },
        props: {
            full_name: String,
            organization_name: String,
            user_role: String,
        },
    }
</script>

<style scoped>
    @import url(../../../css/standard.css);

    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>