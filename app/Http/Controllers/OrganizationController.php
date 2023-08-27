<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Tymon\JWTAuth\Facades\JWTAuth;
use App\Models\Organization;

class OrganizationController extends Controller
{
    public function elections(Request $request) 
    {
        $token = $request->cookie('jwt_token');
        $payload = JWTAuth::setToken($token)->getPayload();
        $studentNumber = $payload->get('StudentNumber');

        // Get the organization member and student by using student_number foreign key
        $organization = Organization::where('StudentNumber', $studentNumber)->first();

     

        
        if ($organization) {
        return Inertia::render('Organization/Elections', [
            //'full_name' => $full_name,
            //'organization_name' => $organization_name,
        ]);
        }
        else {
            return response()->json(['user' => auth('organization')->user()]);
        }
    }

}
