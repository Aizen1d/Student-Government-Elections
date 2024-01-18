<?php

namespace App\Http\Middleware;

use Closure;
use Exception;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\TokenExpiredException;
use Tymon\JWTAuth\Exceptions\TokenInvalidException;
use Tymon\JWTAuth\Exceptions\JWTException;

class CheckAuthComelec
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {   
        $token = $request->cookie('jwt_token');

        try {
            // If not yet logged out
            if ($request->cookie('user_info')) { 
                // Get user role and restrict & redirect back if not comelec
                $user_info_cookie = json_decode($request->cookie('user_info'), true);
                $user_role = $user_info_cookie['user_role'];

                if ($user_role !== 'comelec') {
                    return redirect('organization/elections');
                }
            }
            else {
                // If logged out by the user by clicking the logout button
                if ($request->cookie('logout_pass')) {
                    $logout_cookie = cookie()->forget('logout_pass');
                    return redirect()->route('view.login')->withCookie($logout_cookie);
                }
                
                // If token was expired, not logged out
                return redirect()->route('view.login')->with('token_invalid', 'Your authentication token has expired. Please login again.');
            }
        } 
        catch(Exception $e) {

        }
    
        return $next($request);
    }
}
