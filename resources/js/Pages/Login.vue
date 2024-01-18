<template>
    <div class="container">
        <div class="card">
            <div class="alert alert-danger" role="alert" v-if="invalid">
                {{ invalid }}
            </div>
            <h2>Login</h2>

                <label for="student_number">Student Number</label>
                <input type="text" id="student_number" placeholder="Enter your student number" maxlength="15" @keyup.enter="submitForm" v-model="form.StudentNumber">

                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Enter your password" @keyup.enter="submitForm" v-model="form.Password">

                <button class="login-button" @click.prevent="submitForm" :disabled="loggingIn">{{ login_text }}</button>
        </div>
    </div>

    <title>Login - Election Management</title>
</template>

<script>
    import axios from 'axios';
    import Body from '../Shared/Body.vue';

    export default {
        components: { Body },
        data() {
            return {
                form: {
                    StudentNumber: '',
                    Password: ''
                },
                loggingIn: false,
                invalid: '',
                login_text: 'Login',
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
                if (this.loggingIn) {
                    return;
                }
                if (this.form.StudentNumber === '') {
                    this.invalid = 'Please enter your student number.';
                    return;
                }
                if (this.form.Password === '') {
                    this.invalid = 'Please enter your password.';
                    return;
                }

                this.loggingIn = true;
                this.login_text = 'Logging in...';

                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/election-management/login`, {
                        StudentNumber: this.form.StudentNumber,
                        Password: this.form.Password
                    })
                    .then(response => {
                        if (response.data.message === true) {
                            const user_role = response.data.user_role;

                            axios.post(`/login/auth/${user_role}`, this.form)
                                .then(response => {
                                    if (response.data.redirect) {
                                        window.location.href = response.data.redirect;
                                    }
                                    else if (response.data.invalid) {
                                        this.invalid = response.data.invalid;

                                        this.loggingIn = false;
                                        this.login_text = 'Login';
                                    }
                                })
                                .catch(error => {
                                    // Too many requests, via throttle middleware of Laravel
                                    if (error.response) {
                                        if (error.response.status === 429) { 
                                            const retryAfter = error.response.headers['retry-after'];
                                            this.startCountdown(retryAfter);
                                        }
                                        else if (error.response.status === 419) {
                                            this.invalid = 'Please refresh your page and try again.';
                                        }
                                        else {
                                            // handle other errors
                                        }
                                    }

                                    this.loggingIn = false;
                                    this.login_text = 'Login';
                                });
                        }
                        else {
                            this.invalid = 'Invalid credentials.';
                            this.loggingIn = false;
                            this.login_text = 'Login';
                        }
                    })
                    .catch(error => {
                        console.log(error)

                        // Too many requests, via throttle middleware of Laravel
                        if (error.response) {
                            if (error.response.status === 429) { 
                                const retryAfter = error.response.headers['retry-after'];
                                this.startCountdown(retryAfter);
                            }
                            else if (error.response.status === 419) {
                                this.invalid = 'Please refresh your page and try again.';
                            }
                            else {
                                // handle other errors
                            }
                        }

                        this.loggingIn = false;
                        this.login_text = 'Login';
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

<style scoped>
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
        background-color: #B90321;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .login-button:hover{
        background-color: #a0031d;
    }

    .login-button:disabled {
        background-color: #ccc;
        cursor: default;
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
