<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Organization;
use Illuminate\Support\Facades\Auth;
use App\Models\Election;

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
            'student_number' => $student_number,
            'organization_id' => $organization_id,
            'organization_name' => $organization_name,
            'officer_position_id' => $officer_position_id,
            'user_role' => 'organization',
            'full_name' => $full_name,
        ]);    
    }

    public function electionsCreate() {
        return Inertia::render('Organization/ElectionsCreate');
    }

    public function electionsView(Request $request) 
    { 
        $id = $request->id;
        $electionTable = Election::where('ElectionId', $id)->first();

        if (!$id) {
            // Implement a return a message feature here soon
            return redirect()->route('organization.elections');
        }

        if (!$electionTable) {
            // Implement a return a message feature here soon
            return redirect()->route('organization.elections');
        }

        return inertia('Organization/ElectionsView', [
            'id' => $id,
        ]);
    }
}
