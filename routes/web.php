<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\ComelecController;
use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;

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
Route::fallback(function () {
    return inertia('404');
});

Route::get('/429', function () {
    return inertia('429TooManyRequests');
});

Route::get('/get/token', function () {
    $token = csrf_token();
    return response()->json(['token' => $token]);
});

// Public routes
Route::group(['middleware' => 'public.routes'], function () {
    Route::get('/', [AuthController::class, 'view_login'])
        ->name('root');

    Route::get('/login', [AuthController::class, 'view_login'])
        ->name('view.login');

    Route::post('/register/comelec', [AuthController::class, 'register_comelec'])
        ->name('register.comelec');

    Route::post('/login/auth', [AuthController::class, 'auth_login'])
        ->name('auth.login');
        //->middleware('throttle:5,3'); // 5 attempts in 3 minutes
});

// Routes that are protected by JWT auth
Route::group(['middleware' => 'check.jwt.token'], function () {
    Route::get('/comelec/elections', [ComelecController::class, 'elections'])
        ->name('comelec.elections');
    Route::get('/comelec/insert-data', [ComelecController::class, 'insert_data'])
        ->name('comelec.insert.data');
});

