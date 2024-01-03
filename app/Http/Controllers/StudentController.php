<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Student;
use App\Models\Election;
use Inertia\Inertia;

class StudentController extends Controller
{
    public function home(Request $request)
    {
        $get_user_info = json_decode($request->cookie('voting_user_info'), true);

        $student = Student::where('StudentNumber', $get_user_info['student_number'])
            ->first();

        $student_number = $student->StudentNumber;

        $first_name = $student->FirstName;
        $last_name = $student->LastName;
        $middle_name = $student->MiddleName;

        $course = $student->Course;

        // get full name and check if middle name is null
        if ($middle_name == null) {
            $full_name = $first_name . ' ' . $last_name;
        } else {
            $full_name = $first_name . ' ' . $middle_name . ' ' . $last_name;
        }

        return Inertia::render('Home', [
            'student_number' => $student_number,
            'full_name' => $full_name,
            'course' => $course,
        ]);
    }

    public function votingProcess(Request $request)
    {
        $id = $request->id;
        $electionTable = Election::where('ElectionId', $id)->first();

        if (!$id) {
            return redirect()->route('home');
        }

        if (!$electionTable) {
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

        // Retrieve the student number from the session
        $student_number = $request->session()->get('student_number');

        return Inertia::render('VotingPreview', [
            'id' => $id,
            'votes' => $votes,
            'student_number' => $student_number,
        ]);
    }

}
