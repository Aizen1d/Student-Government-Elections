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
        Schema::create('Code', function (Blueprint $table) {
            $table->id('CodeId');

            $table->string('StudentNumber', 15);
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->text('CodeValue');
            $table->string('CodeType');
            $table->dateTime('CodeExpirationDate');
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Code');
    }
};
