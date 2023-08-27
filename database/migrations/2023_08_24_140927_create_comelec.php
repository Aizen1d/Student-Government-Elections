<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('Comelec', function (Blueprint $table) {
            $table->id('ComelecId');
            $table->string('student_number')->unique();
            $table->foreign('student_number')->references('student_number')->on('Student');
            $table->string('password');
            $table->string('Position');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Comelec');
    }
};
