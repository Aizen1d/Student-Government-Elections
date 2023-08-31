<script>
import { Link } from '@inertiajs/vue3'
import { computed } from 'vue'
import { useUserStore } from '../Stores/UserStore.js'

export default {
    setup() {
        const userStore = useUserStore();

        const linkHref = computed(() => {
            if (userStore.user_role === 'comelec') {
                return '/comelec/elections';
            } 
            else if (userStore.user_role === 'organization') {
                return '/organization/elections';
            }
        });

        return {
            user_role: userStore.user_role,
            linkHref,
        };
    },
    components: {
        Link,
    },
    methods: {
        isUrl(...urls) {
            let currentUrl = this.$page.url.substr(1)
            if (urls[0] === '') {
                return currentUrl === ''
            }
            return urls.filter((url) => currentUrl.startsWith(url)).length
        },
    },
}

</script>

<template>
    <nav id="sidebarMenu" class="collapse d-lg-block sidebar">
        <div class="sidebar-header">
            <span class="sidebar-header-title">Election Management System</span>
        </div>
        <div class="position-sticky">
            <div class="list-group list-group-flush mx-3">
            <Link :href="linkHref" class="main list-group-item py-2"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/elections.svg" alt="Icon" height="35" width="35">
                <span>Elections</span>
            </Link>

            <template v-if="user_role === 'comelec'">
                <Link href="/comelec/insert-data" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/insert_data.svg" alt="Icon" height="35" width="35">
                    <span>Insert Data</span>
                </Link>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/approval.svg" alt="Icon" height="35" width="35">
                    <span>Approvals</span>
                </a>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/announcements.svg" alt="Icon" height="35" width="35">
                    <span>Announcements</span>
                </a>

                <a href="/comelec/rules-and-guidelines" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/rules.svg" alt="Icon" height="35" width="35">
                    <span>Rules & Guidelines</span>
                </a>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/debates.svg" alt="Icon" height="35" width="35">
                    <span>Debates & Open Forum</span>
                </a>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/directory.svg" alt="Icon" height="35" width="35">
                    <span>Directory</span>
                </a>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/appeal.svg" alt="Icon" height="35" width="35">
                    <span>Appeal Review</span>
                </a>

                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="../../images/icons/reports.svg" alt="Icon" height="35" width="35">
                    <span>Reports</span>
                </a>
                
                <a href="" class="main list-group-item py-2"  aria-expanded="true">
                    <img class="side-icon" src="" alt="?" height="35" width="35">
                    <span>Appointments</span>
                </a>
            </template>
            </div>
        </div>
    </nav>
</template>

<style scoped>
body{
    background-color: #EDF2F4;
}

.sidebar-header-title{
    font-family: 'Source Sans Pro Black', sans-serif;
    font-size: 23px;
    color: white;
    font-weight: bolder;
}

.sidebar-header{
    width: 100%;
    height: 10%;
    background-color: #B90321;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.side-icon{
    filter: invert(1);
    margin-right: 5%;
    margin-bottom: 3%;
}

.sidebar {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    padding: 0 0 0; /* padding from top of navbar */
    box-shadow: rgba(0, 0, 0, 0.07) 4.8px 4.8px 13.2px;
    width: 15vw;
    font-size: 17px; 
    z-index: 999;
}

#sidebarMenu{
    background-color: #B90321;
}

.bg{
    background-color: #B90321;
}

@media (max-width: 991.98px) {
    .sidebar {
        width: 100%;
    }
}

.sidebar {
    border-radius: 5px;
    box-shadow: 0 2px 5px 0 rgb(0 0 0 / 16%), 0 2px 10px 0 rgb(0 0 0 / 12%);
}

.sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: 0.5rem;
    overflow-x: hidden;
    overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

.list-group-item{
    position: relative;
    border: transparent;
    transition: margin-left .4s;
    color: #d3d3d3;
    font-family: 'Just Sans', sans-serif;
    font-size: 100%;
    margin-top: 4%;
    background-color: #B90321;
}

.list-group-item:hover{
    background-color: #B90321;
    margin-left: 15px;
    color: white;
}

.active{
    color: white;
}

.sub{
    padding-left: 13%;
}
</style>