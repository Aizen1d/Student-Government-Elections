<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PublicController extends Controller
{
    public function home() {
        return inertia('Home');
    }

    public function rulesAndGuidelines() {
        return inertia('RulesAndGuidelines');
    }
}
