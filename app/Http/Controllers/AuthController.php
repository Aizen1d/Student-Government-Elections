<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use App\Models\Comelec;

class AuthController extends Controller
{    
    public function view_login()
    {
        return inertia('Login');
    }

    public function auth_login(Request $request)
    {   
        $user = (auth('comelec')->attempt
                        ([
                            'student_number' => $request->student_number, 
                            'password' => $request->password
                        ]));

        if ($user){
            $token = $user;
            $cookie_minutes_lifetime = 3;
            //$cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime);
            $cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');
    
            return response()->json([
                'redirect' => '/comelec/elections',
            ])->withCookie($cookie); 
        }

        return response()->json(['message' => 'Invalid credentials.']);
    }
      

    public function register_comelec(Request $request)
    {   
        Comelec::create([
            'student_number' => $request->input('student_number'),
            'password' => Hash::make($request->input('password')),
            'Position' => $request->input('position'),
        ]);

        return response()->json(['message' => 'Comelec successfully inserted.']);
    }
}
