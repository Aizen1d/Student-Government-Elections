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
        Schema::create('Election', function (Blueprint $table) {
            $table->id('ElectionId');
            $table->string('ElectionName');
            $table->string('ElectionType');
            $table->string('ElectionStatus');
            $table->string('SchoolYear');
            $table->string('Semester');
            $table->string('CreatedBy');
            $table->foreign('CreatedBy')->references('StudentNumber')->on('Student');

            $table->datetime('ElectionStart');
            $table->datetime('ElectionEnd');
            $table->datetime('CoCFilingStart');
            $table->datetime('CoCFilingEnd');
            $table->datetime('CampaignStart');
            $table->datetime('CampaignEnd');
            $table->datetime('VotingStart');
            $table->datetime('VotingEnd');
            $table->datetime('AppealStart');
            $table->datetime('AppealEnd');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Elections');
    }
};
