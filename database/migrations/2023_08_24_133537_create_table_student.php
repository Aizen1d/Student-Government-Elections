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
        Schema::create('Student', function (Blueprint $table) {
            $table->id('StudentId');
            $table->string('StudentNumber', 15)->unique();
            $table->string('FirstName');
            $table->string('MiddleName')->nullable();
            $table->string('LastName');
            $table->string('EmailAddress')->unique();
            $table->date('BirthDate');
            $table->string('Course');
            $table->string('CurrentSemesterEnrolled');
            $table->string('YearEnrolled');
            $table->boolean('IsOfficer');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Student');
    }
};
