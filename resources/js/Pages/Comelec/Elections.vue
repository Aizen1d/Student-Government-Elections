<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="container">
        <h1>Elections</h1>
        <p>Full name: {{ full_name }}</p>
        <p>Position: {{ position }}</p>
    </div>
</template>

<script>
    import { Link } from '@inertiajs/vue3'
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
        components: { Link, Navbar, Sidebar },
        props: {
            full_name: String,
            position: String,
            user_role: String,
        },
    }
</script>

<style>
    @import url(../../../css/standard.css);

    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>