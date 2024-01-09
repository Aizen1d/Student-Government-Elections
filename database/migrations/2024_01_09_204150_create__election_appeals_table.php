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
        Schema::create('ElectionAppeals', function (Blueprint $table) {
            $table->id('ElectionAppealsId');

            $table->string('StudentNumber', 15);
            $table->foreign('StudentNumber')->references('StudentNumber')->on('Student');

            $table->text('AppealDetails');
            $table->text('AppealResponse')->nullable();
            $table->string('AppealStatus')->default('Pending');
            $table->string('AttachmentAssetId')->nullable();

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('ElectionAppealsId');
    }
};
