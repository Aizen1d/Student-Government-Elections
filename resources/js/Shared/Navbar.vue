<template>
    <nav class="navbar navbar-expand-lg nav navbar-dark">
        <div class="container-fluid">
            <h1 class="system mx-5 my-2">PUPQC COMELEC Portal</h1>

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
                        <a class="nav-link content mx-5" href="#">DIRECTORY</a>
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
    .active{
        color: #eace2c !important;
    }
    .nav{
        background-color: #B90321;
        padding: 1% 0 1% 0;
    }

    .system{
        color: white;
        font-size: 23px;
        font-family: 'Source Sans Pro Black', sans-serif;
        font-weight: 800;
    }

    .content{
        color: white;
        font-size: 18px;
    }

    .content:active,
    .content:hover,
    .content:focus{
        color: #eace2c;
    }

    .sections{
        justify-content: end !important;
    }

</style>