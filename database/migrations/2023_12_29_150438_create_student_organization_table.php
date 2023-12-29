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
        Schema::create('StudentOrganization', function (Blueprint $table) {
            $table->id('StudentOrganizationId');
            $table->string('OrganizationLogo');
            $table->string('OrganizationName');
            $table->string('OrganizationMemberRequirements');

            $table->string('AdviserImage');
            $table->string('AdviserName');
            $table->string('Vision')->nullable();
            $table->string('Mission')->nullable();

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('StudentOrganization');
    }
};
