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
        Schema::table('Election', function (Blueprint $table) {
            $table->unsignedBigInteger('StudentOrganizationId')->after('ElectionName');
            $table->foreign('StudentOrganizationId')->references('StudentOrganizationId')->on('StudentOrganization');

            $table->dropColumn('ElectionType');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('Election', function (Blueprint $table) {
            $table->dropColumn('StudentOrganizationId');
            $table->string('ElectionType')->after('ElectionName');
        });
    }
};
