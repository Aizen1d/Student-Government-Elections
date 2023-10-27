<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use App\Models\Announcements;
use App\Models\Elections;

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

    public function electionsViewFileCoc(Request $request) {
        $id = $request->id;
        $election = Elections::where('ElectionId', $id)->first();
        $electionName = $election->ElectionName;

        if (!$election) {
            return redirect()->route('elections');
        }

        if (!$id) {
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
        $electionName = $election->ElectionName;

        if (!$election) {
            return redirect()->route('elections');
        }

        if (!$id) {
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

    public function rulesAndGuidelines() {
        return inertia('RulesAndGuidelines');
    }
}
