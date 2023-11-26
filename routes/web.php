<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\StudentController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

// Public routes
Route::group(['middleware' => 'public.routes'], function () {

    Route::get('/', [AuthController::class, 'viewLogin'])
        ->name('root');

    Route::get('/login', [AuthController::class, 'viewLogin'])
        ->name('view.login');

    Route::post('/login/auth', [AuthController::class, 'authLogin'])
        ->name('auth.login')
        ->middleware('throttle:5,3'); // 5 attempts within 3 minutes only

});

Route::group(['middleware' => 'check.auth.student'], function () {

    Route::get('/home', [StudentController::class, 'home'])
        ->name('home');

    Route::get('/voting/process', [StudentController::class, 'votingProcess'])
        ->name('voting.process');

    Route::get('/voting/preview', [StudentController::class, 'votingPreview'])
        ->name('voting.preview');

});