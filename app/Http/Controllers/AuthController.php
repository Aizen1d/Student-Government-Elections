<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use App\Models\Comelec;
use App\Models\Organization;
use Tymon\JWTAuth\Facades\JWTAuth;
use Exception;

class AuthController extends Controller
{    
    public function viewLogin()
    {
        return inertia('Login');
    }

    public function authLogin(Request $request)
    {
        $cookie_minutes_lifetime = 3; // Expiry of the cookie that contains the jwt token
        $guards = [
            'comelec' => '/comelec/elections',
            'organization' => '/organization/elections'
        ];

        // Attempt to login whether comelec or organization user
        foreach ($guards as $guard => $redirect) {
            if ($token = auth($guard)->attempt(['StudentNumber' => $request->StudentNumber, 'password' => $request->Password])) {
                // Store auth user's info to an encrypted cookie
                $cookie_data = [
                    'student_number' => $request->StudentNumber,
                    'user_role' => $guard,
                ];

                $cookie_data = json_encode($cookie_data);
               
                $user_info_cookie = cookie('user_info', $cookie_data, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');
                $cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');

                return response()->json(['redirect' => $redirect])->withCookie($cookie)->withCookie($user_info_cookie);
            }
        }

        return response()->json(['invalid' => 'Invalid student number or password.']);
    } 

    public function logout(Request $request) {
        try { 
            // Instruct client side to delete the cookies with withCookie() and redirect to login page
            $cookie = cookie()->forget('jwt_token');
            $user_info_cookie = cookie()->forget('user_info');

            return response()->json([
                'logout' => 'true',
            ])->withCookie($user_info_cookie)->withCookie($cookie);
            
        }
        catch(Exception $e) {
            return back()->withError($e->getMessage());
        }
    }
    
      
    public function registerComelec(Request $request)
    {   
        try {
            Comelec::create([
                'StudentNumber' => $request->input('StudentNumber'),
                'Password' => Hash::make($request->input('Password')),
                'Position' => $request->input('Position'),
            ]);

            return response()->json(['message' => 'Comelec successfully inserted.']);
        }
        catch(Exception $e) {
            return response()->json(['Something went wrong:' => $e->getMessage()]);
        }
    }

    public function registerOrganization(Request $request)
    {   
        try {
            Organization::create([
                'StudentNumber' => $request->input('StudentNumber'),
                'OfficerPositionId' => $request->input('OfficerPositionId'),
                'OrganizationName' => $request->input('OrganizationName'),
                'Password' => Hash::make($request->input('Password')),
            ]);

            return response()->json(['message' => 'Organization member successfully inserted.']);
        }
        catch(Exception $e) {
            return response()->json(['Something went wrong:' => $e->getMessage()]);
        }
    }
}
