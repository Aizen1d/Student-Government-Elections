<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

use Tymon\JWTAuth\Facades\JWTAuth;

use function Termwind\render;

class PublicRoutes
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Get the JWT token from the cookie
        try {
            $token = $request->cookie('jwt_token');
        }
        catch (\Exception $e) {
            return render('view.login');
        }

        // Check if the token is valid
        if ($token && JWTAuth::setToken($token)->check()) {
            // The user is authenticated with a JWT token, redirect them back to where they came from
            return back();
        }

        $response = $next($request);
        $response->headers->set('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate');
        $response->headers->set('Pragma', 'no-cache');
        $response->headers->set('Expires', 'Fri, 01 Jan 1990 00:00:00 GMT');

        return $response;
    }
}
