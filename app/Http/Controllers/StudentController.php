<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Student;
use Inertia\Inertia;

class StudentController extends Controller
{
    public function home(Request $request)
    {
        $get_user_info = json_decode($request->cookie('user_info'), true);

        $student = Student::where('StudentNumber', $get_user_info['student_number'])
            ->first();

        $student_number = $student->StudentNumber;

        $first_name = $student->FirstName;
        $last_name = $student->LastName;
        $middle_name = $student->MiddleName;

        // get full name and check if middle name is null
        if ($middle_name == null) {
            $full_name = $first_name . ' ' . $last_name;
        } else {
            $full_name = $first_name . ' ' . $middle_name . ' ' . $last_name;
        }

        return Inertia::render('Home', [
            'student_number' => $student_number,
            'full_name' => $full_name,
        ]);
    }

    public function votingProcess()
    {
        return inertia('VotingProcess');
    }

    public function votingPreview()
    {
        return inertia('VotingPreview');
    }
}
