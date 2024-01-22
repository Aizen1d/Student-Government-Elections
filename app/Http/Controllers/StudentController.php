<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Student;
use App\Models\Election;
use App\Models\StudentOrganization;
use App\Models\VotingsTracker;
use Inertia\Inertia;

class StudentController extends Controller
{
    public function home(Request $request)
    {
        $student_number = $request->session()->get('student_number');

        return Inertia::render('Home', [
            'student_number' => $student_number,
        ]);
    }

    public function votingProcess(Request $request)
    {
        $id = $request->id;
        $electionTable = Election::where('ElectionId', $id)->first();

        if (!$id || !$electionTable) {
            return redirect()->route('home');
        }

        // Check if in Voting Period

        $now = date('Y-m-d H:i:s');
        $votingStart = $electionTable->VotingStart;
        $votingEnd = $electionTable->VotingEnd;

        if ($now <= $votingStart) {
            return redirect()->route('home');
        }

        if ($now > $votingEnd) {
            return redirect()->route('home');
        }

        return Inertia::render('VotingProcess', [
            'id' => $id,
        ]);
    }

    public function votingPreview(Request $request)
    {   
        $id = $request->id;
        $votes = $request->votes;

        if (!$id || !$votes) {
            // If there's no id or votes in the request, try to get them from the session
            $id = $request->session()->get('id', $id);
            $votes = $request->session()->get('votes', $votes);
        }

        if (!$id || !$votes) {
            return redirect()->back();
        }

        // Store the id and votes in the session
        $request->session()->put('id', $id);
        $request->session()->put('votes', $votes);

        // Check if student course is same as election course
        $electionTable = Election::where('ElectionId', $id)->first();

        $student_number = $request->session()->get('student_number');

        // Check if in Voting Period

        $now = date('Y-m-d H:i:s');
        $votingStart = $electionTable->VotingStart;
        $votingEnd = $electionTable->VotingEnd;

        if ($now <= $votingStart) {
            return redirect()->route('home');
        }

        if ($now > $votingEnd) {
            return redirect()->route('home');
        }

        return Inertia::render('VotingPreview', [
            'id' => $id,
            'votes' => $votes,
            'student_number' => $student_number,
        ]);
    }

}
