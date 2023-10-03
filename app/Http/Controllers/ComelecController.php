<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Comelec;

class ComelecController extends Controller
{   
    // Landing page for Comelec after logging in
    public function elections(Request $request) 
    {
        $get_user_info = json_decode($request->cookie('user_info'), true);

        $comelec = Comelec::where('StudentNumber', $get_user_info['student_number'])
            ->with('getStudentByStudentNumber')
            ->first();

        $student = $comelec->getStudentByStudentNumber;

        // Comelec columns
        $comelec_id = $comelec->ComelecId;
        $student_number = $comelec->StudentNumber;
        $position = $comelec->Position;

        // Student columns
        $first_name = $student->FirstName;
        $middle_name = $student->MiddleName;
        $last_name = $student->LastName;
        $full_name = $first_name . ' ' . ($middle_name ? $middle_name . ' ' : '') . $last_name;
        $email_address = $student->EmailAddress;

        return Inertia::render('Comelec/Elections', [
            'comelec_id' => $comelec_id,
            'student_number' => $student_number,
            'full_name' => $full_name,
            'position' => $position,
            'user_role' => 'comelec',
        ]);
               
    }

    public function electionsCreate() 
    { 
        return inertia('Comelec/ElectionsCreate');
    }

    public function electionsView(Request $request) 
    { 
        $id = $request->id;

        if (!$id) {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.elections');
        }

        return inertia('Comelec/ElectionsView', [
            'id' => $id,
        ]);
    }

    public function insertData() 
    { 
        return inertia('Comelec/InsertData');
    }

    public function announcements() 
    { 
        return inertia('Comelec/Announcement');
    }

    public function rulesAndGuidelines() 
    { 
        return inertia('Comelec/RulesAndGuidelines');
    }
}
