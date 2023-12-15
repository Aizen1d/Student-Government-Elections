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
        Schema::create('CreatedAdminSignatory', function (Blueprint $table) {
            $table->id('CreatedAdminSignatoryId');

            $table->unsignedBigInteger('CertificationId');
            $table->foreign('CertificationId')->references('CertificationId')->on('Certifications');

            $table->string('SignatoryName');
            $table->string('SignatoryPosition');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('CreatedAdminSignatory');
    }
};
