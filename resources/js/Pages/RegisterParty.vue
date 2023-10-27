<template>
    <Navbar></Navbar>

    <div class="main">
        <div class="header row">
            <div class="col">
                <h1>REGISTER PARTY LIST</h1>
            </div>
            <div class="col btns">
                <button class="mx-4 cancel">Cancel</button>
                <button>Submit</button>
            </div>
        </div>

        <h1>{{ electionName }}</h1>

        <form action="">
            <div class="row pl g-5">
                <div class="col-6">
                    <div class="info">
                        <h6>Party List Information</h6>

                        <label class="form-label" for="name">Name</label>
                        <input class="form-control margin" type="text" name="name">

                        <label class="form-label" for="contact">Cellphone Number</label>
                        <input class="form-control margin" type="text" name="contact">

                        <label for="desc" class="form-label">Description</label>
                        <textarea class="form-control margin" type="text" name="desc"></textarea>

                        <label for="mission" class="form-label">Mission</label>
                        <textarea class="form-control margin" type="text" name="mission"></textarea>

                        <label for="vision" class="form-label">Vision</label>
                        <textarea class="form-control margin" type="text" name="vision"></textarea>

                        <label for="plat" class="form-label">Platforms</label>
                        <textarea class="form-control margin" type="text" name="plat"></textarea>
                    </div>
                </div>
                <div class="col-6">
                    <div class="members">
                        <h6>Attachments</h6>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue'
    import Standards from '../Shared/Standards.vue'

    import { ref } from 'vue'

    export default {
        setup(props) {
            const id = ref(Number(props.id))
            const electionName = ref(props.electionName)

            console.log(electionName.value)

            return {
                id,
                electionName
            }
        },
        props: {
            id: '',
            electionName: 'ss',
        },
        components: {
            Navbar,
            Standards
        },
        methods: {
            cancel(){
                router.visit(`/elections/view?id=${this.id}`)
            }
        }
    }

</script>

<style scoped>
    .main{
        margin: 3% 5%;
        font-family: 'Source Sans Pro', sans-serif;
    }

    .header{
        margin-bottom: 2%;
    }

    .header h1{
        font-size: 28px;
        font-weight: 800;
        height: 100%;
        align-items: center;
        display: flex;
    }

    .btns{
        text-align: end;
    }

    .btns button.cancel{
        background-color: #FDD5D5;
    }

    .btns button{
        font-size: 18px;
        padding-top: 20px;
        padding-bottom: 20px;
        padding: 15px 70px;
        border: transparent;
        border-radius: 8px;
        background-color: #B90321;
        color: #FCFDFD;
    }

    .pl{
        font-family: 'Source Sans Pro', sans-serif;
    }

    .info, .members{
        background-color: #F5F8F9;
        padding: 3%;
        border-radius: 10px;
    }

    .info h6, .members h6{
        font-weight: bold;
        font-size: 20px;
    }

    .form-label{
        margin: 1% 0%;
    }

    .margin{
        margin-bottom: 2%;
        margin-left: 0%;
    }

    .info textarea{
        resize: none;
        overflow-y: auto;
        height: 150px;
    }
</style>