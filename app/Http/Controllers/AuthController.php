<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use App\Models\Student;
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
        $cookie_minutes_lifetime = 120; // Expiry of the cookie that contains the jwt token
      
        $cookie_data = [
            'student_number' => $request->StudentNumber,
            'user_role' => 'student',
        ];

        $cookie_data = json_encode($cookie_data);

        $token = 'Authorized';
        $redirect = '/voting/process';
        
        $user_info_cookie = cookie('user_info', $cookie_data, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');
        $cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');

        return response()->json(['redirect' => $redirect])->withCookie($cookie)->withCookie($user_info_cookie);
    } 

    public function logout(Request $request) {
        try { 
            // Instruct client side to delete the cookies with withCookie() and redirect to login page
            $cookie = cookie()->forget('jwt_token');
            $user_info_cookie = cookie()->forget('user_info');
            $logout_cookie = cookie('logout_pass', 'true', 1);

            return response()->json([
                'logout' => 'true',
            ])->withCookie($user_info_cookie)->withCookie($cookie)->withCookie($logout_cookie);
            
        }
        catch(Exception $e) {
            return back()->withError($e->getMessage());
        }
    }
}
