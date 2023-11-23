<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class StudentController extends Controller
{
    public function votingProcess()
    {
        return inertia('VotingProcess');
    }
}
