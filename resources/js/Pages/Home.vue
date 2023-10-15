<template>
    <Navbar></Navbar>

    <div class="container-margin">
        <div class="container-fluid main">
            <img src="../../images/Home/comelec.jpg" class="main-ann" alt="">
        </div>

        <div class="coc">
            <div class="coc-info">
                <div class="row g-5">
                    <div class="col-6">
                        <div class="coc-pic">
                            <img src="../../images/Home/coc.jpg" alt="" width="400px">
                        </div>
                    </div>
                    <div class="col-6 vertical">
                        <div class="info">
                            <h1>CAMPUS LEADERSHIP: COC NOW OR NEVER!</h1>

                            <p class="py-4">Ready to embark on this epic journey of leading our beloved university? 
                                Your COC is your ticket to the adventure – seize it now and let the campus transformation begin!
                            </p>

                            <button>Ready, Set, COC: Transform the Campus!</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="register">
            <div class="reg-info">
                <div class="row g-5">
                    <div class="col-6 vertical">
                        <div class="r-info">
                            <h1>REGISTER YOUR PARTY, IGNITE THE HEAT!</h1>

                            <p class="py-4">Ready to ignite the political fire? Register your dynamic party list, 
                                and let's set the school ablaze with your passionate campaign. 
                                Register now!
                            </p>

                            <button>Ignite Now: Register Your Party!</button>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="reg-pic">
                            <img src="../../images/Home/register.jpg" alt="" width="400px">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Standards from '../Shared/Standards.vue'
    import Navbar from '../Shared/Navbar.vue'

    export default {
        setup() {
            return {
                
            }
        },
        components: {
            Standards,
            Navbar,
        }
    }

</script>

<style scoped>
    .main{
        margin: 0px auto;
        margin-top: 3%; 
        margin-left: auto;
        margin-right: auto;
        max-width: 113rem;
        height: 55vh;
        min-height: 44.25rem;
        object-fit: cover;
    }

    .main-ann{
        width: 100%;
        height: 100%;
    }

    .container-margin{
        margin-left: 5%;
        margin-right: 5%;
    }

    .coc, .register{
        background-color: #e9b825;
        margin: 10% 0%;
    }

    .coc-info, .reg-info{
        margin: 0% 3% 0% 3%;
        padding: 5% 0%;

    }

    .coc-pic img, .reg-pic img{
        width: 100%;
        height: 50vh;
        object-fit: cover;
        border-radius: 7px;
    }

    .info{
        margin-left: 3%;
    }

    .r-info{
        margin-right: 3%;
    }

    .info h1, .r-info h1{
        font-family: 'Source Sans Pro Black', sans-serif;
        font-weight: 800;
        font-size: 50px;
        color: #880000;
    }

    .info p, .r-info p{
        font-size: 30px;
    }

    .info button, .r-info button{
        width: 100%;
        padding: 3% 0%;
        font-size: 30px;
        border: transparent;
        background-color: #880000;
        color: white;
    }

    .vertical{
        display: flex;
        align-items: center;
    }
</style>