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
        Schema::create('CoC', function (Blueprint $table) {
            $table->id('CoCId');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');

            $table->string('StudentNumber', 15)->unique();
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->string('VerificationCode');
            $table->text('Address');
            $table->string('PoliticalAffiliation');

            $table->unsignedBigInteger('PartyListId')->nullable();
            $table->foreign('PartyListId')->references('PartyListId')->on('PartyList');

            $table->string('SelectedPositionName');
            $table->string('DisplayPhoto');
            $table->string('CertificationOfGrades');
            $table->string('Status');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('CoC');
    }
};
