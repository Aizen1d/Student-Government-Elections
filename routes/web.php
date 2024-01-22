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

Route::get('/elections/view/rankings', [PublicController::class, 'electionsViewRankings'])
->name('elections.view.rankings');

Route::get('/elections/view/winners', [PublicController::class, 'electionsViewWinners'])
->name('elections.view.winners');

Route::get('/elections/view/file-coc', [PublicController::class, 'electionsViewFileCoc'])
->name('elections.view.file.coc');

Route::get('/elections/view/register-party', [PublicController::class, 'electionsViewRegisterParty'])
->name('elections.view.register.party');

Route::get('/announcements', [PublicController::class, 'announcements'])
->name('announcements');

Route::get('/announcements/view', [PublicController::class, 'announcementsView'])
->name('announcements.view');

Route::get('/directory', [PublicController::class, 'directory'])
->name('directory');

Route::get('/directory/voters', [PublicController::class, 'directoryVoters'])
->name('directory.voters');

Route::get('/directory/voters/view', [PublicController::class, 'directoryVotersView'])
->name('directory.voters.view');

Route::get('/directory/candidates', [PublicController::class, 'directoryCandidates'])
->name('directory.candidates');

Route::get('/directory/candidates/view', [PublicController::class, 'directoryCandidatesView'])
->name('directory.candidates.view');

Route::get('/directory/partylists', [PublicController::class, 'directoryPartylists'])
->name('directory.partylists');

Route::get('/directory/partylists/selection', [PublicController::class, 'directoryPartylistsSelection'])
->name('directory.partylists.selection');

Route::get('/directory/partylists/view', [PublicController::class, 'directoryPartylistsView'])
->name('directory.partylists.view');

Route::get('/directory/student-organization', [PublicController::class, 'directoryStudentOrganization'])
->name('directory.student.organization');

Route::get('/directory/student-organization/view', [PublicController::class, 'directoryStudentOrganizationView'])
->name('directory.student.organization.view');

Route::get('/rules-and-guidelines', [PublicController::class, 'rulesAndGuidelines'])
->name('rules.and.guidelines');
