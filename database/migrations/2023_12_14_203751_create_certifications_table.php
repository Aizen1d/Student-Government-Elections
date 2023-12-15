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
        Schema::create('Certifications', function (Blueprint $table) {
            $table->id('CertificationId');
            $table->string('Title');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');

            $table->date('Date');
            $table->string('AdminSignatoryQuantity');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Certifications');
    }
};
