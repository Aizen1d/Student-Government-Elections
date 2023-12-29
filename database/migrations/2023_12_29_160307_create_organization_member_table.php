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
        Schema::create('OrganizationMember', function (Blueprint $table) {
            $table->id('OrganizationMemberId');

            $table->unsignedBigInteger('StudentOrganizationId');
            $table->foreign('StudentOrganizationId')->references('StudentOrganizationId')->on('StudentOrganization');

            $table->string('StudentNumber', 15)->unique();
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');
            
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('OrganizationMember');
    }
};
