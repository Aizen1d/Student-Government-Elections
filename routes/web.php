<?php

use App\Http\Controllers\PublicController;
use Illuminate\Support\Facades\Route;

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

Route::get('/', function () {
    return inertia('Home');
});

Route::get('/home', [PublicController::class, 'home'])
->name('home');

Route::get('/elections', [PublicController::class, 'elections'])
->name('elections');

Route::get('/elections/view', [PublicController::class, 'electionsView'])
->name('elections.view');

Route::get('/elections/view/file-coc', [PublicController::class, 'electionsViewFileCoc'])
->name('elections.view.file.coc');

Route::get('/elections/view/register-party', [PublicController::class, 'electionsViewRegisterParty'])
->name('elections.view.register.party');

Route::get('/announcements', [PublicController::class, 'announcements'])
->name('announcements');

Route::get('/announcements/view', [PublicController::class, 'announcementsView'])
->name('announcements.view');

Route::get('/rules-and-guidelines', [PublicController::class, 'rulesAndGuidelines'])
->name('rules.and.guidelines');
