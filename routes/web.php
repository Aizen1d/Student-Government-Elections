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

    Route::post('/login/auth/comelec', [AuthController::class, 'authComelecLogin'])
        ->name('auth.login.comelec')
        ->middleware('throttle:5,3'); // 5 attempts within 3 minutes only

    Route::post('/login/auth/officer', [AuthController::class, 'authOfficerLogin'])
        ->name('auth.login.officer')
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

    Route::get('/comelec/elections/create', [ComelecController::class, 'electionsCreate'])
        ->name('comelec.elections.create');

    Route::get('/comelec/elections/view', [ComelecController::class, 'electionsView'])
        ->name('comelec.elections.view');

    Route::get('/comelec/voters-registration', [ComelecController::class, 'votersRegistration'])
        ->name('comelec.voters.registration');

    Route::get('/comelec/voters-registration/queues', [ComelecController::class, 'votersRegistrationQueues'])
        ->name('comelec.voters.registration.queues');

    Route::get('/comelec/approvals', [ComelecController::class, 'approvals'])
        ->name('comelec.approvals');

    Route::get('/comelec/approvals/view', [ComelecController::class, 'approvalsView'])
        ->name('comelec.approvals.view');

    Route::get('/comelec/announcements', [ComelecController::class, 'announcements'])
        ->name('comelec.announcements');

    Route::get('/comelec/rules-and-guidelines', [ComelecController::class, 'rulesAndGuidelines'])
        ->name('comelec.rules.and.guidelines');

    Route::get('/comelec/directory', [ComelecController::class, 'directory'])
        ->name('comelec.directory');

    Route::get('/comelec/directory/election-winners', [ComelecController::class, 'directoryElectionWinners'])
        ->name('comelec.directory.election.winners');

    Route::get('/comelec/directory/student-organizations', [ComelecController::class, 'directoryStudentOrganizations'])
        ->name('comelec.directory.student.organizations');

    Route::get('/comelec/directory/certifications', [ComelecController::class, 'directoryCertifications'])
        ->name('comelec.directory.certifications');

    Route::get('/comelec/directory/certifications/create', [ComelecController::class, 'directoryCertificationsCreate'])
        ->name('comelec.directory.certifications.create');

    Route::get('/comelec/appeal-review', [ComelecController::class, 'appealReview'])
        ->name('comelec.appeal.review');

    Route::get('/comelec/reports', [ComelecController::class, 'reports'])
        ->name('comelec.reports');

    Route::get('/comelec/appointments', [ComelecController::class, 'appointments'])
        ->name('comelec.appointments');
});

// Routes that are protected by JWT token and must be authenticated as organization user
Route::group(['middleware' => 'check.auth.organization'], function () {

    Route::get('/organization/elections', [OrganizationController::class, 'elections'])
    ->name('organization.elections');

    Route::get('/organization/elections/create', [OrganizationController::class, 'electionsCreate'])
    ->name('organization.elections.create');

    Route::get('/organization/elections/view', [OrganizationController::class, 'electionsView'])
    ->name('organization.elections.view');
});
