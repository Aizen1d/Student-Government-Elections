<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Illuminate\Support\Facades\Route;

use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\TokenExpiredException;
use Tymon\JWTAuth\Exceptions\TokenInvalidException;
use Tymon\JWTAuth\Exceptions\JWTException;

class CheckJWTToken
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
            if (JWTAuth::setToken($token)->check()) {
                return $next($request);
            }
        } 
        catch (TokenExpiredException $e) {
            // Im using cookie lifetime so token expiration is nothing, for now?..
            return redirect()->route('view.login');
        } 
        catch (TokenInvalidException $e) {
            return redirect()->route('view.login')->with('token_invalid', 'Your token was invalid/expired. Please login again.');
        } 
        catch (JWTException $e) {
            return redirect()->route('view.login');
        }

    }
}
