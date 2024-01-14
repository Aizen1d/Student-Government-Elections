<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Comelec;
use App\Models\Election;
use App\Models\CoC;
use App\Models\PartyList;
use App\Models\ElectionAppeals;

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
        $electionTable = Election::where('ElectionId', $id)->first();

        if (!$id) {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.elections');
        }

        if (!$electionTable) {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.elections');
        }

        return inertia('Comelec/ElectionsView', [
            'id' => $id,
        ]);
    }

    public function votersRegistration() 
    { 
        return inertia('Comelec/VotersRegistration');
    }

    public function votersRegistrationQueues() 
    { 
        return inertia('Comelec/VotersRegistrationQueues');
    }

    public function approvals() 
    { 
        return inertia('Comelec/Approvals');
    }

    public function approvalsView(Request $request) 
    { 
        $type = $request->type;
        $id = $request->id;

        if ($type === 'coc') {
            $checkIfExisting = CoC::where('CoCId', $id)->first();
        }
        else if ($type === 'party-list') {
            $checkIfExisting = PartyList::where('PartyListId', $id)->first();
        }
        else {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.approvals');
        }

        if (!$id) {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.approvals');
        }

        if (!$checkIfExisting) {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.approvals');
        }

        if ($type === 'coc') {
            return inertia('Comelec/ApprovalsViewCoC', [
                'type' => $type,
                'id' => $id,
            ]);
        }
        else if ($type === 'party-list') {
            return inertia('Comelec/ApprovalsViewParty', [
                'type' => $type,
                'id' => $id,
            ]);
        }
        else {
            // Implement a return a message feature here soon
            return redirect()->route('comelec.approvals');
        }
    }

    public function announcements() 
    { 
        return inertia('Comelec/Announcement');
    }

    public function rulesAndGuidelines() 
    { 
        return inertia('Comelec/RulesAndGuidelines');
    }

    public function directory() 
    { 
        return inertia('Comelec/Directory');
    }

    public function directoryElectionWinners() 
    { 
        return inertia('Comelec/DirectoryElectionWinners');
    }

    public function directoryStudentOrganizations() 
    { 
        return inertia('Comelec/DirectoryStudentOrganizations');
    }

    public function directoryCertifications() 
    { 
        return inertia('Comelec/DirectoryCertifications');
    }

    public function directoryCertificationsCreate() 
    { 
        return inertia('Comelec/DirectoryCertificationsCreate');
    }

    public function appealReview() 
    { 
        return inertia('Comelec/AppealReview');
    }

    public function reports() 
    { 
        return inertia('Comelec/Reports');
    }

    public function appointments() 
    { 
        return inertia('Comelec/Appointments');
    }
}
