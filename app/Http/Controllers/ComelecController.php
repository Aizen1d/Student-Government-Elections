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
            'full_name' => $full_name,
            'position' => $position,
            'user_role' => 'comelec',
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
