<template>
    <title>Reports - EMS</title>
    <Sidebar></Sidebar>
    <Navbar></Navbar>

    <div class="components">
        <div class="header">
            <h1 class="page-title">REPORTS</h1>
        </div>
        
        <div class="row" style="margin-left: -1%;">
            <div class="col-12">
                <BaseContainer :height="'auto'" :maxHeight="'600px'" style="padding-left: 25px; padding-top: 25px; padding-bottom: 20px; width: 101.5%;">
                    <div class="row">
                        <div class="col-4" style="display: flex; align-items: center;">
                            <select class="form-select" aria-label="Default select example" v-model="select_election_input" @change="electionInputChanged">
                                <option value="" disabled hidden selected>Select Election</option>
                                <option v-if="!isElectionsDataLoading" v-for="(election, index) in electionsData" :key="index" :value="election.ElectionId">
                                    {{ election.ElectionName }}
                                </option>
                            </select>
                        </div>

                        <div class="col-8" style="display: flex; align-items: center;">
                            <img :src="selected_election_logo" alt="" class="election-logo">
                            <span class="election-title">{{ selected_election_name }}</span>
                        </div>

                        <hr class="line">

                    </div>
                    <div class="row">
                        <div class="col-3" style="display: flex; align-items: center;">
                            <span class="election-metadata">Semester:</span>
                            <span class="election-data mx-2">{{ selected_election_semester }}</span>
                        </div>
                        <div class="col-3" style="display: flex; align-items: center;">
                            <span class="election-metadata">School Year:</span>
                            <span class="election-data mx-2">{{ selected_election_school_year }}</span>
                        </div>
                        <div class="col-3" style="display: flex; align-items: center;">
                            <span class="election-metadata">Course Requirement:</span>
                            <span class="election-data mx-2">{{ selected_election_course_requirement }}</span>
                        </div>
                        <div class="col-3" style="display: flex; align-items: center;">
                            <span class="election-metadata">Current Period:</span>
                            <span class="election-data mx-2">{{ selected_election_current_period }}</span>
                        </div>

                    </div>
                </BaseContainer>
            </div>
        </div>

        <div class="row" style="margin-top: 20px; margin-left: -25.8px;">
            <div class="col-4">
                <BaseContainer :height="'auto'" :maxHeight="'600px'">
                    <div class="row">
                        <div class="col-12">
                            <div class="card-information">
                                <img src="../../../images/analytics/candidate.svg" alt="" class="card-svg">
                                <div class="count">
                                    <span class="quantity">{{ selected_election_candidates }}</span>
                                    <span class="quantity-label">Candidates</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </BaseContainer>
                <BaseContainer :height="'auto'" :maxHeight="'600px'" style="margin-top: 3.5%; margin-bottom: 3.5%;">
                    <div class="row">
                        <div class="col-12">
                            <div class="card-information">
                                <img src="../../../images/analytics/party.svg" alt="" class="card-svg">
                                <div class="count">
                                    <span class="quantity">{{ selected_election_partylist }}</span>
                                    <span class="quantity-label">Party List</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </BaseContainer>
                <BaseContainer :height="'auto'" :maxHeight="'600px'" class="">
                    <div class="row">
                        <div class="col-12">
                            <div class="card-information">
                                <img src="../../../images/analytics/position.svg" alt="" class="card-svg">
                                <div class="count">
                                    <span class="quantity">{{ selected_election_voters_population }}</span>
                                    <span class="quantity-label">Voters Population</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </BaseContainer>
            </div>
            <div class="col-4 px-3">
                <BaseContainer :height="'auto'" :maxHeight="'600px'">
                    <div class="col-12">
                        <div class="chart-container">
                            <canvas id="voter-turnout-chart" style="margin-top: 5%;"></canvas>
                        </div>
                    </div>
                </BaseContainer>
            </div>
            <div class="col-4">
                <BaseContainer :height="'auto'" :maxHeight="'600px'">
                    <div class="col-12">
                        <div class="chart-container">
                            <canvas id="voter-course-chart" style="margin-top: 5%;"></canvas>
                        </div>
                    </div>
                </BaseContainer>
            </div>
        </div>

        <div class="header">
            <h1 class="page-title" style="margin-top: 2%;">Registration Approvals</h1>
        </div>

        <div class="row" style="margin-top: 15px; margin-left: -23px;">
            <div class="col-6" style="padding-right: 1.15%;">
                <BaseContainer :height="'auto'" :maxHeight="'600px'">
                    <div class="col-12">
                        <div class="chart-container">
                            <canvas id="coc-chart" style="margin-top: 2.5%;"></canvas>
                        </div>
                    </div>
                </BaseContainer>
            </div>
            <div class="col-6" style="padding-left: 1.15%;">
                <BaseContainer :height="'auto'" :maxHeight="'600px'">
                    <div class="col-12">
                        <div class="chart-container">
                            <canvas id="partylist-chart" style="margin-top: 2.5%;"></canvas>
                        </div>
                    </div>
                </BaseContainer>
            </div>
        </div>

        <div class="header">
            <h1 class="page-title" style="margin-top: 2%;">Candidates</h1>
        </div>

        <div class="row" style="margin-left: -1%;">
            <div class="col-12">
                <BaseContainer :height="'auto'" :maxHeight="'600px'" style="padding-left: 25px; padding-top: 25px; padding-bottom: 20px; width: 101.5%;">
                    <div class="row">
                        <div class="col-4" style="display: flex; align-items: center;">
                            <select class="form-select" aria-label="Default select example" v-model="select_election_input" @change="electionInputChanged">
                                <option value="" disabled hidden selected>Select Election</option>
                                <option v-if="!isElectionsDataLoading" v-for="(election, index) in electionsData" :key="index" :value="election.ElectionId">
                                    {{ election.ElectionName }}
                                </option>
                            </select>
                        </div>

                        <hr class="line">

                    </div>
                    <div class="row">
                        <div class="col-6" style="display: flex; align-items: center;">
                                <div class="candidate-wrapper">
                                    <div class="candidate-information">
                                        <img src="../../../images/candidate2.jpg" alt="" class="candidate-img">
                                        <div class="candidate-description">
                                            <div class="spacing">
                                                <span class="candidate-name">David Daniel D. Reataza</span>
                                            </div>
                                            <span class="etc">Independent</span>
                                            <span class="etc">BSIT 3-1</span>
                                            <span class="motto">“Empowering Students, Building Futures”</span>
                                            <span class="platform-label">PLATFORM:</span>
                                            <p class="platform">
                                                Academic Excellence: Advocate for resources and programs that enhance the academic experience and help students reach their full potential.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                        </div>
                        <div class="col-6" style="display: flex; align-items: center;">
                            
                        </div>
                    </div>
                </BaseContainer>
            </div>
        </div>

    </div>

    <div style="margin-top: 2%;"></div>
</template>

<script>
    import { router } from '@inertiajs/vue3'
    import { ref, watch, watchEffect } from 'vue';

    import Navbar from '../../Shared/Navbar.vue';
    import Sidebar from '../../Shared/Sidebar.vue';
    import ActionButton from '../../Shared/ActionButton.vue';
    import BaseContainer from '../../Shared/BaseContainer.vue';
    import BaseTable from '../../Shared/BaseTable.vue';
    import ImageSkeleton from '../../Skeletons/ImageSkeleton.vue';

    import { useQuery } from "@tanstack/vue-query";
    import axios from 'axios';
    
    export default {
        setup() {
            const select_election_input = ref('');
            const initial_election_selected = ref(false);
            
            const selected_election_logo = ref('');
            const selected_election_name = ref('');
            const selected_election_semester = ref('');
            const selected_election_school_year = ref('');
            const selected_election_course_requirement = ref('');
            const selected_election_current_period = ref('');
            
            const selected_election_candidates = ref('');
            const selected_election_partylist = ref('');
            const selected_election_voters_population = ref('');

            const fetchElections = async () => {
                const response = await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/election/all`);
                console.log(`Elections table fetched successfully. Duration: ${response.duration}`)

                select_election_input.value = response.data.elections[0].ElectionId;
                initial_election_selected.value = true;

                return response.data.elections;
            }

            const { data: electionsData, 
                    isLoading: isElectionsDataLoading,
                    isSuccess: isElectionsDataSuccess } = 
                    useQuery({
                        queryKey: ['fetchElections'],
                        queryFn: fetchElections,
                    });

            const instance_voter_turnout = null;
            const data_voter_turnout = ref([
                { 
                    value: 0, 
                    label: 'Active Voters', 
                    color: '#C9FFC5', 
                    borderColor: '#70AD47'
                },
                { 
                    value: 0, 
                    label: 'Inactive Voters', 
                    color: 'rgba(255, 99, 132, 0.4)', 
                    borderColor: 'rgba(255, 99, 132, 1)' 
                },
            ]);
            
            const instance_voter_course = null;
            const data_voter_course = [
                { 
                    value: 0, 
                    label: 'BBTLEDHE', 
                    color: '#C9FFC5', // Green
                    borderColor: '#70AD47'
                },
                { 
                    value: 0, 
                    label: 'BSBAHRM', 
                    color: 'rgba(255, 99, 132, 0.4)', // Red
                    borderColor: 'rgba(255, 99, 132, 1)' 
                },
                {
                    value: 0,
                    label: 'BSBA-MM',
                    color: 'rgba(255, 159, 64, 0.4)', // Orange
                    borderColor: 'rgba(255, 159, 64, 1)'
                },
                {
                    value: 0,
                    label: 'BSENTREP',
                    color: 'rgba(75, 192, 192, 0.4)', // Teal
                    borderColor: 'rgba(75, 192, 192, 1)'
                },
                {
                    value: 0,
                    label: 'BSIT',
                    color: 'rgba(54, 162, 235, 0.4)', // Blue
                    borderColor: 'rgba(54, 162, 235, 1)'
                },
                {
                    value: 0,
                    label: 'BPAPFM',
                    color: 'rgba(255, 235, 79, 0.4)', // Yellow
                    borderColor: 'rgba(255, 235, 59, 1)' 
                },
                {
                    value: 0,
                    label: 'DOMTMOM',
                    color: 'rgba(153, 102, 255, 0.4)', // Purple
                    borderColor: 'rgba(153, 102, 255, 1)'
                }
            ];

            const instance_coc = null;
            const data_coc = [
                { 
                    value: 22, 
                    label: 'Approved', 
                    color: '#C9FFC5', 
                    borderColor: '#70AD47'
                },
                { 
                    value: 19, 
                    label: 'Rejected', 
                    color: 'rgba(255, 99, 132, 0.4)', 
                    borderColor: 'rgba(255, 99, 132, 1)' 
                },
            ];

            const instance_partylist = null;
            const data_partylist = [
                { 
                    value: 22, 
                    label: 'Approved', 
                    color: '#C9FFC5', 
                    borderColor: '#70AD47'
                },
                { 
                    value: 19, 
                    label: 'Rejected', 
                    color: 'rgba(255, 99, 132, 0.4)', 
                    borderColor: 'rgba(255, 99, 132, 1)' 
                },
            ];
            
            return {
                select_election_input,
                initial_election_selected,
                selected_election_logo,
                selected_election_name,
                selected_election_semester,
                selected_election_school_year,
                selected_election_course_requirement,
                selected_election_current_period,
                selected_election_candidates,
                selected_election_partylist,
                selected_election_voters_population,

                electionsData,
                isElectionsDataLoading,
                isElectionsDataSuccess,

                instance_voter_turnout,
                data_voter_turnout,

                instance_voter_course,
                data_voter_course,

                instance_coc,
                data_coc,

                instance_partylist,
                data_partylist,
            }
        },
        components: {
            Navbar,
            Sidebar,
            ActionButton,
            BaseContainer,
            BaseTable,
            ImageSkeleton,
        },
        mounted() {
            const voter_turnout_chart = document.getElementById('voter-turnout-chart');
            const voter_course_chart = document.getElementById('voter-course-chart');

            const coc_chart = document.getElementById('coc-chart');
            const partylist_chart = document.getElementById('partylist-chart');

            Chart.register(ChartDataLabels);

            this.instance_voter_turnout = new Chart(voter_turnout_chart, {
                type: 'doughnut',
                data: {
                    labels: this.data_voter_turnout.map(item => item.label),
                    datasets: [{
                        label: 'Total',
                        data: this.data_voter_turnout.map(item => item.value),
                        backgroundColor: this.data_voter_turnout.map(item => item.color),
                        borderColor: this.data_voter_turnout.map(item => item.borderColor),
                        borderWidth: 1,
                        hoverOffset: 20
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        enabled: true
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Voters Population',
                            font: {
                                size: 15,
                                family: 'Inter',
                            },
                            padding: {
                                bottom: 20
                            },
                            align: 'middle'
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                usePointStyle: true,
                                boxWidth: 15,
                                boxHeight: 8,
                                padding: 20,
                                font: {
                                    size: 15,
                                }
                            }
                        },
                        datalabels: {
                            formatter: this.getPercentageInGraph,
                            color: 'black',
                            font: {
                                size: 13,
                            }
                        }
                    },
                    layout: {
                        padding: {
                            bottom(voter_turnout_chart) {
                                const chart = voter_turnout_chart.chart;
                                let pb = 0;
                                    chart.data.datasets.forEach(function(el) {
                                    const hOffset = el.hoverOffset || 0;
                                    pb = Math.max(hOffset / 2 + 5, pb)
                                });
                                
                                return pb + 10;
                            },
                        }
                    },
                },
            });
            
            this.instance_voter_course = new Chart(voter_course_chart, {
                type: 'bar',
                data: {
                    labels: this.data_voter_course.map(item => item.label),
                    datasets: [{
                        label: '',
                        data: this.data_voter_course.map(item => item.value),
                        backgroundColor: this.data_voter_course.map(item => item.color),
                        borderColor: this.data_voter_course.map(item => item.borderColor),
                        borderWidth: 1,
                        hoverOffset: 20
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        enabled: true
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Voters Course Distribution',
                            font: {
                                size: 15,
                                family: 'Inter',
                            },
                            padding: {
                                bottom: 20
                            },
                            align: 'middle'
                        },
                        legend: {
                            display: false,
                            position: 'bottom',
                            labels: {
                                usePointStyle: true,
                                boxWidth: 15,
                                boxHeight: 8,
                                padding: 20,
                                font: {
                                    size: 15,
                                    family: 'Inter',
                                }
                            }
                        },
                        datalabels: {
                            formatter: this.getPercentageInGraph,
                            color: 'black',
                            font: {
                                size: 13,
                            }
                        }
                    },
                    layout: {
                        padding: {
                            bottom(voter_course_chart) {
                                const chart = voter_course_chart.chart;
                                let pb = 0;
                                    chart.data.datasets.forEach(function(el) {
                                    const hOffset = el.hoverOffset || 0;
                                    pb = Math.max(hOffset / 2 + 5, pb)
                                });
                                
                                return pb + 10;
                            },
                        }
                    },
                },
            });

            this.instance_coc = new Chart(coc_chart, {
                type: 'pie',
                data: {
                    labels: this.data_coc.map(item => item.label),
                    datasets: [{
                        label: 'Total',
                        data: this.data_coc.map(item => item.value),
                        backgroundColor: this.data_coc.map(item => item.color),
                        borderColor: this.data_coc.map(item => item.borderColor),
                        borderWidth: 1,
                        hoverOffset: 20
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        enabled: true
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Certificate of Candidacy',
                            font: {
                                size: 15,
                                family: 'Inter',
                            },
                            padding: {
                                bottom: 20
                            },
                            align: 'middle'
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                usePointStyle: true,
                                boxWidth: 15,
                                boxHeight: 8,
                                padding: 20,
                                font: {
                                    size: 15,
                                }
                            }
                        },
                        datalabels: {
                            formatter: this.getPercentageInGraph,
                            color: 'black',
                            font: {
                                size: 13,
                            }
                        }
                    },
                    layout: {
                        padding: {
                            bottom(coc_chart) {
                                const chart = coc_chart.chart;
                                let pb = 0;
                                    chart.data.datasets.forEach(function(el) {
                                    const hOffset = el.hoverOffset || 0;
                                    pb = Math.max(hOffset / 2 + 5, pb)
                                });
                                
                                return pb + 10;
                            },
                        },
                    },
                },
            });

            this.instance_partylist = new Chart(partylist_chart, {
                type: 'pie',
                data: {
                    labels: this.data_partylist.map(item => item.label),
                    datasets: [{
                        label: 'Total',
                        data: this.data_partylist.map(item => item.value),
                        backgroundColor: this.data_partylist.map(item => item.color),
                        borderColor: this.data_partylist.map(item => item.borderColor),
                        borderWidth: 1,
                        hoverOffset: 20
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        enabled: true
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Party List',
                            font: {
                                size: 15,
                                family: 'Inter',
                            },
                            padding: {
                                bottom: 20
                            },
                            align: 'middle'
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                usePointStyle: true,
                                boxWidth: 15,
                                boxHeight: 8,
                                padding: 20,
                                font: {
                                    size: 15,
                                }
                            }
                        },
                        datalabels: {
                            formatter: this.getPercentageInGraph,
                            color: 'black',
                            font: {
                                size: 13,
                            }
                        }
                    },
                    layout: {
                        padding: {
                            bottom(partylist_chart) {
                                const chart = partylist_chart.chart;
                                let pb = 0;
                                    chart.data.datasets.forEach(function(el) {
                                    const hOffset = el.hoverOffset || 0;
                                    pb = Math.max(hOffset / 2 + 5, pb)
                                });
                                
                                return pb + 10;
                            },
                        },
                    },
                },
            });
        },
        created() {
            watchEffect(() => {
                if (this.initial_election_selected) {
                    this.electionInputChanged();
                }
            });
        },
        methods: {
            electionWinners(){
                router.visit('/comelec/directory/election-winners');
            },
            studentOrganizations(){
                router.visit('/comelec/directory/student-organizations');
            },
            certifications(){
                router.visit('/comelec/directory/certifications');
            },
            getPercentageInGraph(value, chart) {
                if (value >= 1) {
                    let sum = chart.dataset.data.reduce((a, b) => a + b, 0);
                    let percentage = '\n' + (value*100 / sum).toFixed(2)+"%";
                    return percentage;
                } 
                else {
                    return null;
                }
            },
            getPercentageWithLabelInGraph(value, chart) {
                if (value >= 1) {
                    let sum = chart.dataset.data.reduce((a, b) => a + b, 0);
                    let percentage = chart.chart.data.labels[chart.dataIndex] + '\n' + (value*100 / sum).toFixed(2)+"%";
                    return percentage;
                } 
                else {
                    return null;
                }
            },
            async electionInputChanged() {
                await axios.get(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/reports/election/${this.select_election_input}`)
                .then((response) => {
                    const election = response.data.election;

                    this.selected_election_logo = election.StudentOrganizationLogo;
                    this.selected_election_name = election.ElectionName;

                    this.selected_election_semester = election.Semester;
                    this.selected_election_school_year = election.SchoolYear;
                    this.selected_election_course_requirement = election.CourseRequirement;
                    this.selected_election_current_period = election.ElectionPeriod;

                    this.selected_election_candidates = election.NumberOfCandidates;
                    this.selected_election_partylist = election.NumberOfPartylists;
                    this.selected_election_voters_population = election.NumberOfVoters;

                    // update voter turnout chart

                    this.data_voter_turnout = [
                        { 
                            value: election.NumberOfActiveVoters, 
                            label: 'Active Voters', 
                            color: '#C9FFC5', 
                            borderColor: '#70AD47'
                        },
                        { 
                            value: election.NumberOfInactiveVoters, 
                            label: 'Inactive Voters', 
                            color: 'rgba(255, 99, 132, 0.4)', 
                            borderColor: 'rgba(255, 99, 132, 1)' 
                        },
                    ];

                    this.instance_voter_turnout.data.datasets[0].data = this.data_voter_turnout.map(item => item.value);
                    this.instance_voter_turnout.update();

                    // update voter course distribution chart

                    election.CourseDistribution.forEach(course => {
                        const courseName = Object.keys(course)[0];
                        const courseValue = course[courseName];

                        // Find the corresponding object in the data_voter_course array
                        const courseObject = this.data_voter_course.find(item => item.label === courseName);

                        // If the course object exists, update its value
                        if (courseObject) {
                            courseObject.value = courseValue;
                        }
                    });

                    this.instance_voter_course.data.datasets[0].data = this.data_voter_course.map(item => item.value);
                    this.instance_voter_course.update();

                    // update coc chart

                    this.data_coc = [
                        { 
                            value: election.NumberOfApprovedCoC, 
                            label: 'Approved', 
                            color: '#C9FFC5', 
                            borderColor: '#70AD47'
                        },
                        { 
                            value: election.NumberOfRejectedCoC, 
                            label: 'Rejected', 
                            color: 'rgba(255, 99, 132, 0.4)', 
                            borderColor: 'rgba(255, 99, 132, 1)' 
                        },
                    ];

                    this.instance_coc.data.datasets[0].data = this.data_coc.map(item => item.value);
                    this.instance_coc.update();

                    // update partylist chart

                    this.data_partylist = [
                        { 
                            value: election.NumberOfApprovedPartylist + 3, 
                            label: 'Approved', 
                            color: '#C9FFC5', 
                            borderColor: '#70AD47'
                        },
                        { 
                            value: election.NumberOfRejectedPartylist + 2, 
                            label: 'Rejected', 
                            color: 'rgba(255, 99, 132, 0.4)', 
                            borderColor: 'rgba(255, 99, 132, 1)' 
                        },
                    ];

                    this.instance_partylist.data.datasets[0].data = this.data_partylist.map(item => item.value);
                    this.instance_partylist.update();
                })
            },
        }
    }
</script>

<style scoped>
    /*!!!START OF CSS!!!*/
    .line{
        border: 0;
        height: 2px;
        background: rgb(249,249,249);
        background: linear-gradient(90deg, rgba(249,249,249,1) 0%, rgba(217,217,217,1) 50%, rgba(249,249,249,1) 100%);
        margin: 1% 0%;
    }

    .election-logo{
        width: 50px;
    }

    .election-title{
        font-weight: 800;
        font-size: 25px;
        margin-left: 1.5%;
        font-family: 'Inter', sans-serif;
    }

    .election-metadata{
        font-weight: 600;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
    }

    .election-data{
        font-weight: 200;
        font-size: 16px;
        font-family: 'Inter', sans-serif;
    }

    .components{
        margin-left: 18%;
        margin-top: 2%;
        font-family: 'Inter', sans-serif;
        margin-right: 3%;
    }

    .header{
        display: flex;
        align-items: center;
        margin: 0% -1%;
        justify-content: space-between;
    }

    .page-title{
        font-weight: 800;
        font-size: 30px;
        margin: 0%;
        margin-left: 1%;
        font-family: 'Inter', sans-serif;
    }

    .directory{
        margin: 1.5% -1%;
        background-color: white;
        box-shadow: 0px 3px 5px rgba(167, 165, 165, 0.5);
        border-radius: 3px;
        transition: transform 0.4s ease;
    }

    .directory-content{
        padding: 1.5%;
        display: flex;
        align-items: center;
    }

    .select-directory{
        color: black;
        text-decoration: none;
    }

    .select-directory:hover{
        cursor: pointer;
    }

    .logo{
        width: 70px;
        height: 70px;
    }

    .directory-title{
        margin: 0% 0% 0% 2%;
        width: 100%;
        font-weight: 600;
        font-size: 25px;
    }

    .directory:hover{
        color: #B90321;
        background-color: #f4f4f4;

        .logo{
            filter: invert(8%) sepia(80%) saturate(5145%) hue-rotate(2deg) brightness(98%) contrast(114%);
        }
    }   

    .form-control, .form-select, .body {
        border: 1px solid rgba(40, 40, 40, 0.25);
    }

    .card-information{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .count{
        display: flex;
        flex-direction: column;
        text-align: end;
    }

    .card-svg{
        width: 100px;
    }

    .chart-container{
        width: 100%;
        height: 435px;
        display: flex;
        align-items: center;
    }

  

    .quantity{
        font-weight: 800;
        font-size: 45px;
    }

    .quantity-label{
        font-weight: 100;
        font-size: 16px;
    }
    
    .candidate-wrapper{
        padding: 2%;
    }

    .candidate-information{
        display: flex;
    }

    .candidate-img{
        width: 220px;
        height: 300px;
        object-fit: cover;
    }

    .candidate-description{
        margin-left: 3.5%;
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    .candidate-name{
        font-weight: bold;
        font-size: 20px;
    }

    .etc{
        font-size: 16px;
        margin-top: 3px;
        margin-bottom: -5px;
    }

    .motto{
        margin-top: 25px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
    }

    .platform-label{
        font-size: 18px;
        font-weight: bold;
        margin: 30px 0px;
    }

    .platform{
        margin: -20px 0px;
        font-size: 16px;
        text-align: justify;
    }
</style>