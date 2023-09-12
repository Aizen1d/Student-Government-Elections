<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <h2>Elections</h2>
        <div class="row margin">
            <div class="col-2">
                <input type="hidden" name="filter-type">
                        <select class="form-select" aria-label="Default select example" id="filter">
                            <option selected>Filter by</option>
                            <option selected>Semester</option>
                            <option selected>School Year</option>
                        </select>
            </div>
            <div class="col-4">
                <input type="search" id="search" class="form-control" placeholder="Search" aria-label="Search">
            </div>
            <div class="col-6 new">
                <button class="new-btn">Create Election</button>
            </div>      
        </div>   
        
        <div class="list">
            <table class="table table-hover table-bordered border-dark table-responsive">
                <thead class="head">
                    <tr>
                        <th>#</th>
                        <th class="th-sm">Type</th>
                        <th class="th-sm">Name</th>
                        <th class="th-sm">Date Created</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th scope="row">1</th>
                        <th>SSC Election</th>
                        <th>Sample Election</th>
                        <th>September 4, 2023</th>
                    </tr>
                    <tr>
                        <th scope="row">2</th>
                        <th>SSC Election</th>
                        <th>Sample Election</th>
                        <th>September 4, 2023</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div>
            <ul class="pagination">
                <li class="page-item disabled">
                  <a class="page-link navi" href="#" tabindex="-1" aria-disabled="true">Previous</a>
                </li>
                <li class="page-item active" aria-current="page"><a class="page-link page" href="#">1</a></li>
                <li class="page-item disabled">
                  <a class="page-link navi" href="#">Next</a>
                </li>
              </ul>
        </div>
    </div>
</template>

<script>
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import { useUserStore } from '../../Stores/UserStore';

    export default {
        setup(props) {
            // Since this is the landing page for the Comelec after loggin in,
            // We need to set the user's role to comelec in the user store
            const userStore = useUserStore();
            userStore.user_role = props.user_role;
            userStore.full_name = props.full_name;
            
            /*const data = ref('');

            axios.get('http://127.0.0.1:8500/student/all')
                .then(response => {
                    data.value = response.data;
                    console.log(response.data);
                });*/

            return {}
        },
        components: { Navbar, Sidebar },
        props: {
            full_name: String,
            user_role: String,
        },
    }
</script>

<style scoped>
.components{
    margin-left: 18%;
    margin-top: 2%;
    font-family: 'Source Sans', sans-serif;
    margin-right: 3.2%;
}

.components h2{
    font-weight: 800;
    font-size: 28px;
    margin-bottom: 1.5%;
}

.margin{
    margin-right: -1%;
    margin-left: -1%;
}

.new{
    text-align: end;
}

.new-btn{
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 100px 15px 100px;
    border: transparent;
    border-radius: 10px;
    background-color: #B90321;
    color: white;
    margin-right: -1.8%;
}

.list{
    margin-top: 1.5%;
    background-color: white;
    margin: 1.5% -1% 0% -1%;
    padding: 30px 30px 15px 30px;
    border-radius: 7px;
    max-height: 550px;
}


#filter{
    margin-left: -5%;
    width: 100%;
    height: 54px;
    border-radius: 10px;
}

#search{
    margin-left: -4%;
    width: 100%;
    height: 54px;
    border-radius: 10px;
}

.pagination{
    margin-top: 1.5%;
    margin-left: -1.5%;
}

.page-link {
    line-height: 50px;
    padding: 0%;
    margin: 0%;
}

.page-item{
    padding: 5px;
}

.page{
    width: 65px;
    text-align: center;
    border-radius: 5px;
}

.navi{
    width: 95px;
    text-align: center;
    border-radius: 5px;
    background-color: transparent !important;
}
</style>