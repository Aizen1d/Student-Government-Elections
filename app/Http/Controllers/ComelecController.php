<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Comelec;

class ComelecController extends Controller
{
    public function elections(Request $request) 
    {
        $token = $request->cookie('jwt_token');

        // Get the comelec and student by using student_number foreign key
        $comelec = JWTAuth::toUser($token)->with('getStudentByStudentNumber')->first();
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

        /*return response()->json([
            'comelec_id' => $comelec_id,
            'student_number' => $student_number,
            'position' => $position,
            'full_name' => $full_name,
            'email_address' => $email_address,
        ]); */

        return Inertia::render('Comelec/Elections', [
            'FullName' => $full_name,
            'Position' => $position,
        ]);
               
    }

    public function insertData() 
    { 
        return inertia('Comelec/InsertData');
    }
}
