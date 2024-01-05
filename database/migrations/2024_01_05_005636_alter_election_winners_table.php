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
        Schema::table('ElectionWinners', function (Blueprint $table) {
            $table->boolean('IsTied')->default(false);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('ElectionWinners', function (Blueprint $table) {
            $table->dropColumn('IsTied');
        });
    }
};
