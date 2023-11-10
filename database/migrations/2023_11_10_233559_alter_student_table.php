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
        Schema::table('Student', function (Blueprint $table) {
            $table->dropColumn('BirthDate');
            $table->string('Year')->after('EmailAddress');
        });
        
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('Student', function (Blueprint $table) {
            $table->date('BirthDate')->after('Course');
            $table->dropColumn('Year');
        });
    }
};
