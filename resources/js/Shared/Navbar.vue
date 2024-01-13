<template>
    <nav class="navbar navbar-expand-lg nav navbar-dark">
        <div class="navbar-contents">
            <div>
                <img src="../../images/Navbar/puplogo.png" alt="" class="puplogo">
                <img src="../../images/Navbar/portal.png" alt="" class="pcplogo">
            </div>

            <div class="collapse navbar-collapse sections">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <Link href="/home" 
                            :class="{ 'active': $inertia.page.url.startsWith('/home') }" 
                            class="nav-link content mx-5" 
                            aria-current="page">HOME
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link href="/elections" 
                            :class="{ 'active': $inertia.page.url.startsWith('/elections') }" 
                            class="nav-link content mx-5" 
                            aria-current="page">ELECTIONS
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link href="/announcements?type=all" 
                            class="nav-link content mx-5"
                            :class="{ 'active': $inertia.page.url.startsWith('/announcements') }" 
                            >ANNOUNCEMENTS
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link href="/directory" 
                            class="nav-link content mx-5"
                            :class="{ 'active': $inertia.page.url.startsWith('/directory') }" 
                            >DIRECTORY
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link href="/rules-and-guidelines" 
                            class="nav-link content mx-5" 
                            :class="{ 'active': $inertia.page.url.startsWith('/rules-and-guidelines')  }" 
                            >RULES & GUIDELINES
                        </Link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    import { Link } from '@inertiajs/vue3'

    export default {
        setup() {
            return {
                
            }
        },
        components: {
            Link,
        }
    }

</script>

<style scoped>
    .nav{
        background-color: #ffffff;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        padding: 0.6% 0%;
    }

    .active{
        color: #B90321 !important;
    }

    .navbar-contents{
        margin: 0% 8%;
        display: flex;
        align-items: center;
        width: 100%;
        justify-content: space-between;
    }

    .puplogo{
        width: 58px;
    }

    .pcplogo{
        width: 200px;
        margin: 0px 30px;
    }

    .content{
        color: black;
        font-size: 18px;
    }

    .content:hover{
        color: #800000;
    }

    .sections{
        justify-content: end !important;
}

</style>