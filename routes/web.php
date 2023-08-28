<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\ComelecController;
use App\Http\Controllers\OrganizationController;
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

    Route::get('/', [AuthController::class, 'viewLogin'])
        ->name('root');

    Route::get('/login', [AuthController::class, 'viewLogin'])
        ->name('view.login');

    Route::post('/login/auth', [AuthController::class, 'authLogin'])
        ->name('auth.login')
        ->middleware('throttle:5,3'); // 5 attempts within 3 minutes only

    // Exclusives only / dummy data insertion purposes
    Route::post('/register/comelec', [AuthController::class, 'registerComelec'])
        ->name('register.comelec');

    Route::post('/register/organization', [AuthController::class, 'registerOrganization'])
        ->name('register.organization');
});

// Routes that needs to revalidate back history / or no back history
Route::group(['middleware' => 'revalidate'], function () {

    Route::post('/logout', [AuthController::class, 'logout'])
    ->name('post.logout');
});

// Routes that are protected by JWT token and must be authenticated as comelec user
Route::group(['middleware' => 'check.auth.comelec'], function () {

    Route::get('/comelec/elections', [ComelecController::class, 'elections'])
        ->name('comelec.elections');

    Route::get('/comelec/insert-data', [ComelecController::class, 'insertData'])
        ->name('comelec.insert.data');
});

// Routes that are protected by JWT token and must be authenticated as organization user
Route::group(['middleware' => 'check.auth.organization'], function () {

    Route::get('/organization/elections', [OrganizationController::class, 'elections'])
    ->name('organization.elections');
});
