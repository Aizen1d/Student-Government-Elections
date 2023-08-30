<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>
</template>

<script >
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import { useUserStore } from '../../Stores/UserStore';

    export default {
        setup() {
            const userStore = useUserStore();   
            const user_role = userStore.user_role;

            return {user_role}
        },
        components: { Navbar, Sidebar },
        
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