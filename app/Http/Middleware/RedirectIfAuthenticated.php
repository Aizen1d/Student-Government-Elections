<?php

namespace App\Http\Middleware;

use App\Providers\RouteServiceProvider;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

use Tymon\JWTAuth\Facades\JWTAuth;

class RedirectIfAuthenticated
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string ...$guards): Response
    {
        $token = $request->cookie('jwt_token');

        // Check if the token is valid
        if ($token && JWTAuth::setToken($token)->check()) {
            // The user is authenticated with a JWT token, redirect them back to where they came from
            return redirect('/comelec/home');
        }
    
        return $next($request);
    }
}
