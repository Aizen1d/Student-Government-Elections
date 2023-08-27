<template>
    <div class="container">
        <div class="card">
            <div class="alert alert-danger" role="alert" v-if="invalid">
                {{ invalid }}
            </div>
            <h2>Login</h2>

            <form class="login-form" @submit.prevent="submitForm">
                <label for="student_number">Student Number</label>
                <input type="text" id="student_number" placeholder="Enter your student number" v-model="form.StudentNumber">

                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Enter your password" v-model="form.Password">

                <button class="login-button" type="submit">Login</button>
            </form>
        </div>
    </div>

    <title>Login - Election Management</title>
</template>

<script>
    import Navbar from '../Shared/Navbar.vue';
    import Sidebar from '../Shared/Sidebar.vue';
    import axios from 'axios';

    export default {
        components: { Navbar, Sidebar },
        data() {
            return {
                form: {
                    StudentNumber: '',
                    Password: ''
                },
                invalid: '',
                countdown: 0,
                intervalId: null,
            }
        },
        mounted() {
            if (this.$page.props.flash.token_invalid) {
                this.invalid = this.$page.props.flash.token_invalid;
            }
        },
        methods: {
             submitForm() {
                if (this.countdown > 0) {
                    return;
                }
                 axios.post('/login/auth', this.form)
                    .then(response => {
                        if (response.data.redirect) {
                            window.location.href = response.data.redirect;
                        }
                        else if (response.data.invalid) {
                            this.invalid = response.data.invalid;
                        }
                    })
                    .catch(error => {
                        if (error.response && error.response.status === 429) {
                            const retryAfter = error.response.headers['retry-after'];
                            this.startCountdown(retryAfter);
                        } else {
                            // handle other errors
                        }
                    });
            },
            startCountdown(seconds) {
                this.countdown = seconds;
                this.intervalId = setInterval(() => {
                    this.countdown--;
                    if (this.countdown === 0) {
                        clearInterval(this.intervalId);
                        this.invalid = '';
                    } else {
                        this.invalid = `Too many login attempts. Please wait ${this.countdown} seconds before trying again.`;
                    }
                }, 1000);
            },
        }
    };

</script>



<style>
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .card {
        width: 300px;
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    h2 {
        color: #0e0e0e;
        margin-bottom: 20px;
    }

    .login-form {
        display: flex;
        flex-direction: column;
    }

    label {
        text-align: left;
        margin-bottom: 5px;
    }

    input {
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }

    .login-button {
        padding: 10px;
        background-color: #3F518B;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .login-button:hover{
        background-color: #2F4080;
    }

    .switch {
        margin-top: 15px;
        font-size: 14px;
    }
    
    .switch a {
        color: #007bff;
        text-decoration:none
    }
</style>
