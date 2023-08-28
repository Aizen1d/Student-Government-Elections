<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Organization;
use Illuminate\Support\Facades\Auth;

class OrganizationController extends Controller
{
    public function elections(Request $request) 
    {
        $get_user_info = json_decode($request->cookie('user_info'), true);

        $organization = Organization::where('StudentNumber', $get_user_info['student_number'])
            ->with('getStudentByStudentNumber')
            ->first();

        $student = $organization->getStudentByStudentNumber;

        // Organization columns
        $organization_id = $organization->OrganizationId;
        $student_number = $organization->StudentNumber;
        $officer_position_id = $organization->OfficerPositionId;
        $organization_name = $organization->OrganizationName;

        // Student columns
        $first_name = $student->FirstName;
        $middle_name = $student->MiddleName;
        $last_name = $student->LastName;
        $full_name = $first_name . ' ' . ($middle_name ? $middle_name . ' ' : '') . $last_name;
        $email_address = $student->EmailAddress;

        return Inertia::render('Organization/Elections', [
            'full_name' => $full_name,
            'organization_name' => $organization_name,
            'user_role' => 'organization',
        ]);
               
    }
}
