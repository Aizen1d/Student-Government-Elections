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
        Schema::create('Candidates', function (Blueprint $table) {
            $table->id('CandidateId');

            $table->string('StudentNumber', 15)->unique();
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');

            $table->unsignedBigInteger('PartyListId')->nullable();
            $table->foreign('PartyListId')->references('PartyListId')->on('PartyList');

            $table->string('SelectedPositionName');
            $table->string('DisplayPhoto');

            $table->unsignedBigInteger('Rating')->default(0);  
            $table->unsignedBigInteger('TimesRated')->default(0);
            $table->unsignedBigInteger('Votes')->default(0);

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Candidates');
    }
};
