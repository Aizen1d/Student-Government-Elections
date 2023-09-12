<template>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components mb-4">
        <h2>Insert Data</h2>
        
        <form action="">
            <div class="row g-4">
                <div class="col-6">
                    <div class="note">
                        <h6>Manually input student data.</h6>
                    </div>
                    <div class="box">
                        <div class="row mb-2">
                            <div class="col">
                                <label class="form-label" for="stud-num">Student Number</label>
                                <input class="form-control margin" type="text" name="stud-num">
                            </div>
                            <div class="col">
                                <label class="form-label" for="course">Course</label>
                                <input type="hidden" name="course">
                                <select class="form-select" aria-label="Default select example">
                                    <option selected>Select</option>
                                    <option value="1">BBTLEDHE</option>
                                    <option value="2">BSBAHRM</option>
                                    <option value="3">BSBA-MM</option>
                                    <option value="4">BSENTREP</option>
                                    <option value="5">BSIT</option>
                                    <option value="6">BPAPFM</option>
                                    <option value="7">DOMTMOM</option>
                                </select>
                            </div>
                        </div>
                        <label class="form-label" for="f-name">First Name</label>
                        <input class="form-control margin" type="text" name="f-name">
                        
                        <label class="form-label" for="m-name">Middle Name</label>
                        <input class="form-control margin" type="text" name="m-name">

                        <label class="form-label" for="l-name">Last Name</label>
                        <input class="form-control margin" type="text" name="l-name">

                        <div class="row">
                            <div class="col">
                                <label class="form-label" for="email">Email Address</label>
                                <input class="form-control margin mb-3" type="email" name="email">

                                <label class="form-label" for="sem">Current Semester</label>
                                <input class="form-control margin" type="text" name="sem">
                            </div>
                            <div class="col">
                                <label class="form-label" for="bday">Birth Date</label>
                                <input class="form-control margin mb-3" type="date" name="bday">

                                <label class="form-label" for="year">Year Enrolled</label>
                                <input class="form-control margin" type="text" name="year">
                            </div>
                        </div>

                        <div>
                            <div class="row mt-3">
                                <div class="col">
                                    <button class="cancel">Cancel</button>
                                </div>
                                <div class="col">
                                    <button class="insert">Insert</button>
                                </div>
                            </div>
                            
                            
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="note">
                        <h6>Upload CSV/Excel files.</h6>
                    </div>
                    <div class="box">
                        <input class="form-control margin" type="file">
    
                        <div class="drop">
                            <div>
                                <span>Drag and Drop file</span>
                                <br>
                                <img src="upload.svg" width="40px" alt="upload" draggable="false">
                            </div>
                        </div>

                        <button class="mt-4 upload">Upload file</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script >
    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';

    export default {
        components: { Navbar, Sidebar },
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
    margin-bottom: 2%;
    margin-left: 0%;
}

.note{
    margin-top: 1.5%;
    background-color: #FDD5D5;
    padding: 2%;
}

.note h6{
    margin-top: 10px;
}

.box{
    background-color: white;
    padding: 3%;
}

.cancel{
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 100px 15px 100px;
    border: transparent;
    border-radius: 10px;
    background-color: #FDD5D5;
    color: black;
    margin-right: 2%;
    width: 100%;
}

.insert{
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 100px 15px 100px;
    border: transparent;
    border-radius: 10px;
    background-color: #B90321;
    color: white;
    width: 100%;
}

.upload{
    padding-top: 20px;
    padding-bottom: 20px;
    padding: 15px 100px 15px 100px;
    border: transparent;
    border-radius: 10px;
    background-color: #B90321;
    color: white;
    width: 100%;
}

.drop{
    background-color: rgb(243, 243, 243);
    height: 250px;
    border: 2px dashed rgb(205, 205, 205);
    border-radius: 10px;
    color: #BFBFBF;
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center;
}

.drop span{
    -webkit-user-select: none;  /* Chrome, Safari, Opera */
    -moz-user-select: none;     /* Firefox */
    -ms-user-select: none;      /* IE 10+ */
    user-select: none;          /* Standard syntax */    
}

.drop img{
    filter: invert(56%) sepia(100%) saturate(0%) hue-rotate(183deg) brightness(115%) contrast(86%);
    display: block; 
    margin: 0 auto;
}
</style>