<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use App\Models\Announcements;
use App\Models\Elections;
use App\Models\PartyList;
use App\Models\StudentOrganization;

class PublicController extends Controller
{
    public function home() {
        return inertia('Home');
    }

    public function elections() {
        return inertia('Elections');
    }

    public function electionsView(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();

        if (!$election) {
            return redirect()->route('elections');
        }

        if (!$id) {
            return redirect()->route('elections');
        }

        return Inertia::render('ElectionsView', [
            'id' => $id
        ]);
    }

    public function electionsViewRankings(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();

        if (!$id) {
            return redirect()->route('elections');
        }

        if (!$election) {
            return redirect()->route('elections');
        }

        $now = date('Y-m-d H:i:s');
        $votingStart = $election->VotingStart;

        // if the voting has not started yet, redirect to elections
        if ($now < $votingStart) {
            return redirect()->route('elections');
        }

        return Inertia::render('Rankings', [
            'election_id' => $id,
        ]);
    }

    public function electionsViewWinners(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();

        if (!$id) {
            return redirect()->route('elections');
        }

        if (!$election) {
            return redirect()->route('elections');
        }

        // Check if voting ended
        $now = date('Y-m-d H:i:s');
        $votingEnd = $election->VotingEnd;

        // if the voting has not ended yet, redirect to elections
        if ($now < $votingEnd) {
            return redirect()->route('elections');
        }

        return Inertia::render('Winners', [
            'election_id' => $id,
        ]);
    }

    public function electionsViewFileCoc(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();

        if (!$election) {
            return redirect()->route('elections');
        }

        $electionName = $election->ElectionName;

        if (!$id) {
            return redirect()->route('elections');
        }

        // Check if in CoCFilingStart and CoCFilingEnd
        $now = date('Y-m-d H:i:s');
        $cocFilingStart = $election->CoCFilingStart;
        $cocFilingEnd = $election->CoCFilingEnd;

        if ($now < $cocFilingStart) {
            return redirect()->route('elections');
        }

        if ($now > $cocFilingEnd) {
            return redirect()->route('elections');
        }

        return Inertia::render('CoC', [
            'id' => $id,
            'electionName' => $electionName
        ]);
    }

    public function electionsViewRegisterParty(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();

        if (!$election) {
            return redirect()->route('elections');
        }

        $electionName = $election->ElectionName;

        if (!$id) {
            return redirect()->route('elections');
        }

        // Check if in CoCFilingStart and CoCFilingEnd Since it was the same with CoC Filing Date
        $now = date('Y-m-d H:i:s');
        $cocFilingStart = $election->CoCFilingStart;
        $cocFilingEnd = $election->CoCFilingEnd;

        if ($now < $cocFilingStart) {
            return redirect()->route('elections');
        }

        if ($now > $cocFilingEnd) {
            return redirect()->route('elections');
        }

        return Inertia::render('RegisterParty', [
            'id' => $id,
            'electionName' => $electionName
        ]);
    }

    public function announcements(Request $request) {
        $type = $request->query('type', 'none');
    
        $validTypes = ['all', 'elections', 'debates', 'open_forums', 'educational_programs', 'results'];
    
        if (!in_array($type, $validTypes)) {
            // If the type is not valid, redirect to the announcement all page
            return redirect()->route('announcements', ['type' => 'all']);
        }
    
        return Inertia::render('Announcements', [
            'type' => $type
        ]);
    }

    public function announcementsView(Request $request) {
        $id = $request->id;
        $announcement = Announcements::where('AnnouncementId', $id)->first();

        if (!$announcement) {
            return redirect()->route('announcements', ['type' => 'all']);
        }

        if (!$id) {
            return redirect()->route('announcements', ['type' => 'all']);
        }

        return Inertia::render('AnnouncementsView', [
            'id' => $id
        ]);
    }

    public function directory() {
        return inertia('DirectoryList');
    }

    public function directoryVoters() {
        return inertia('DirectoryVoters');
    }

    public function directoryVotersView(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();
        $electionName = $election->ElectionName;

        if (!$election) {
            return redirect()->route('directory.voters');
        }

        if (!$id) {
            return redirect()->route('directory.voters');
        }

        return Inertia::render('DirectoryVotersView', [
            'id' => $id,
            'electionName' => $electionName
        ]);
    }

    public function directoryCandidates() {
        return inertia('DirectoryCandidates');
    }

    public function directoryCandidatesView(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();
        $electionName = $election->ElectionName;

        if (!$election) {
            return redirect()->route('directory.candidates');
        }

        if (!$id) {
            return redirect()->route('directory.candidates');
        }

        return Inertia::render('DirectoryCandidatesView', [
            'id' => $id,
            'electionName' => $electionName
        ]);
    }

    public function directoryPartylists() {
        return inertia('DirectoryPartyList');
    }

    public function directoryPartylistsSelection(Request $request){
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();
        $electionName = $election->ElectionName;

        if (!$election) {
            return redirect()->route('directory.partylists');
        }

        if (!$id) {
            return redirect()->route('directory.partylists');
        }

        return Inertia::render('DirectoryPartyListSelection', [
            'id' => $id,
            'electionName' => $electionName
        ]);
    }

    public function directoryPartylistsView(Request $request) {
        $id = $request->id;
        $partylist = PartyList::where('PartyListId', $id)->first();

        if (!$partylist) {
            return redirect()->route('directory.partylists.selection');
        }

        if (!$id) {
            return redirect()->route('directory.partylists.selection');
        }

        return Inertia::render('DirectoryPartyListView', [
            'id' => $id,
        ]);
    }

    public function directoryStudentOrganization() {
        return inertia('DirectoryStudentOrganization');
    }

    public function directoryStudentOrganizationView(Request $request) {
        $id = $request->id;
        $studentOrganization = StudentOrganization::where('StudentOrganizationId', $id)->first();
        
        if (!$studentOrganization) {
            return redirect()->route('directory.student.organization');
        }

        if (!$id) {
            return redirect()->route('directory.student.organization');
        }

        return Inertia::render('DirectoryStudentOrganizationView', [
            'id' => $id,
        ]);
    }

    public function rulesAndGuidelines() {
        return inertia('RulesAndGuidelines');
    }
}
