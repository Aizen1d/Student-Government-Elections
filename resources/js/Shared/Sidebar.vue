<script>
import { Link } from '@inertiajs/vue3'

export default {
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
            <Link href="/comelec/elections" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/elections.svg" alt="Icon" height="35" width="35">
                <span>Elections</span>
            </Link>
            <Link href="/comelec/insert-data" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/insert_data.svg" alt="Icon" height="35" width="35">
                <span>Insert Data</span>
            </Link>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/approval.svg" alt="Icon" height="35" width="35">
                <span>Approvals</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/announcements.svg" alt="Icon" height="35" width="35">
                <span>Announcements</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/rules.svg" alt="Icon" height="35" width="35">
                <span>Rules & Guidelines</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/debates.svg" alt="Icon" height="35" width="35">
                <span>Debates & Open Forum</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/directory.svg" alt="Icon" height="35" width="35">
                <span>Directory</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/appeal.svg" alt="Icon" height="35" width="35">
                <span>Appeal Review</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="../../images/icons/reports.svg" alt="Icon" height="35" width="35">
                <span>Reports</span>
            </a>
            <a href="" class="main list-group-item list-group-item-action py-2 ripple bg 
                    {{ ? 'active' : '' }}"  aria-expanded="true">
                <img class="side-icon" src="" alt="?" height="35" width="35">
                <span>Appointments</span>
            </a>
            
            </div>
        </div>
    </nav>
</template>

<style>
@import url(../../css/standard.css);

.sidebar-header-title{
    font-family: 'Just Sans ExBold', sans-serif;
    font-size: 120%;
    color: white;
}

.sidebar-header{
    width: 100%;
    height: 10%;
    background-color: var(--dark_blue) !important;
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

.side-icon:hover {
    filter: invert(99%) sepia(0%) saturate(1104%) hue-rotate(181deg) brightness(84%) contrast(100%);

}

.sidebar {
    position: fixed;
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
    background-color: var(--light_blue);
}

.bg{
    background-color: var(--light_blue);
}

@media (max-width: 991.98px) {
    .sidebar {
        width: 100%;
    }
}

.sidebar .active {
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
    color: var(--light_white);
    font-family: var(--side_bar_font);
    font-size: 100%;
    margin-top: 4%;
}

.list-group-item:hover{
    background-color: var(--light_blue);
    margin-left: 15px;
    color: white;
}

.active{
    position: relative;
    border: transparent;
    color: white;
}

.sub{
    padding-left: 13%;
}
</style>