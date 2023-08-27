<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use App\Models\Comelec;
use Exception;

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
                            'StudentNumber' => $request->StudentNumber, 
                            'password' => $request->Password // use small p in password because it's required by the attempt method
                        ]));

        if ($user) {
            $token = $user;
            $cookie_minutes_lifetime = 3;
            //$cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime);
            $cookie = cookie('jwt_token', $token, $cookie_minutes_lifetime, null, null, true, true, false, 'strict');
    
            return response()->json([
                'redirect' => '/comelec/elections',
            ])->withCookie($cookie); 
        } 
        else {
            return response()->json(['invalid' => 'Invalid student number or password.',]);
        }
    }
      

    public function register_comelec(Request $request)
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
}
