<template>
    <div class="main">
        <div class="col-md-4 login-section">
            <div class="login-label">
                <h1 class="login-label-back">voter login</h1>
                <h1 class="login-label-front">VOTER LOGIN</h1>
            </div>

            <div class="alert alert-danger" style="text-align: center; margin-top: 3%;" role="alert" v-if="invalid">
                {{ invalid }}
            </div>

            <div class="credentials">
                <div class="form-group">
                    <label class="form-label" for="student-number">Student Number</label>
                    <input class="form-control" type="text" name="student-number" placeholder="Enter your student number" maxlength="15" @keyup.enter="submitForm" v-model="form.StudentNumber">
                </div>
                <div class="form-group my-4">
                    <label class="form-label" for="password">Password</label>
                    <input class="form-control" type="password" name="password" placeholder="Enter your password" @keyup.enter="submitForm" v-model="form.Password">
                </div>

                <div class="login">
                    <button class="login-button" @click.prevent="submitForm" :disabled="loggingIn">{{ login_text }}</button>
                </div>
            </div>
        </div>
        <div class="col-md design">
            <img src="../../images/login-image.svg" alt="" class="login-image" draggable="false">
        </div>
    </div>

    <title>Login - Voting System</title>
</template>

<script>
    import axios from 'axios';
    import Body from '../Shared/Body.vue';

    export default {
        components: { Body },
        data() {
            return {
                form: { StudentNumber: '',
                        Password: '',
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
                    axios.post(`${import.meta.env.VITE_FASTAPI_BASE_URL}/api/v1/student/voting/login`, {
                        StudentNumber: this.form.StudentNumber,
                        Password: this.form.Password
                    })
                    .then(response => {
                        if (response.data.message === true) {

                            axios.post('/login/auth', this.form)
                            .then(response => {
                                if (response.data.redirect) {
                                    window.location.href = response.data.redirect;
                                }
                            })
                            .catch(error => {
                                console.log(error)
                            });
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
    .main{
        font-family: 'Inter', sans-serif;
    }

    .login-section{
        background-color: #FFFDFA;
        float: left;
        padding: 10% 0%;
        height: 100vh;
    }

    .login-label{
        text-align: center;
    }

    .login-label-back {
        margin: 0%;
        font-weight: 900;
        font-size: 4.5vw; /* Adjust this value as needed */
        color: #F7F7F7;
        position: relative;
    }

    .login-label-front {
        margin: 0%;
        font-weight: 900;
        font-size: 2.1vw; /* Adjust this value as needed */
        position: absolute;
        top: 13vw; /* Adjust this value to position the front label correctly */
        left: 9.7vw;
        z-index: 1;
    }

    .credentials{
        margin: 5% 0%;
    }

    .form-group{
        padding: 0% 15%;
    }

    .form-control:focus {
        border-color: #FFD966; /* Change this to your desired color */
        box-shadow: 0 0 0 0.2rem rgba(246, 177, 1, 0.25); /* Change this to match your desired color */
    }

    .login{
        text-align: center;
        margin: 5% 0%;
    }

    .login-button{
        width: 70%;
        border: transparent;
        background-color: #FFD966;
        color: white;
        font-weight: 900;
        font-size: 20px;
        height: 45px;
        border-radius: 6px;   
    }

    .design{
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .login-image{
        width: 600px;
    }
</style>
