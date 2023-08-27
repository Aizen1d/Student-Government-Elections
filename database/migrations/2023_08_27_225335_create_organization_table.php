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
        Schema::create('Organization', function (Blueprint $table) {
            $table->id('OrganizationId');

            $table->string('StudentNumber', 15)->unique();
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->unsignedBigInteger('OfficerPositionId')->unique();
            $table->foreign('OfficerPositionId')->references('OfficerPositionId')->on('OfficerPosition');

            $table->string('OrganizationName');
            $table->string('Password');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Organization');
    }
};
