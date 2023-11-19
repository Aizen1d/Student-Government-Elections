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
        Schema::create('RatingsTracker', function (Blueprint $table) {
            $table->id('RatingsTrackerId');
            
            $table->string('StudentNumber', 15)->unique();
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('RatingsTracker');
    }
};
