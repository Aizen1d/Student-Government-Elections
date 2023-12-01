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
        Schema::create('ElectionAnalytics', function (Blueprint $table) {
            $table->id('ElectionAnalyticsId');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');    
            
            $table->unsignedBigInteger('AbstainCount')->default(0);
            $table->unsignedBigInteger('VotesCount')->default(0);

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('ElectionAnalytics');
    }
};
