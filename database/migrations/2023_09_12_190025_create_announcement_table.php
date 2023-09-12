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
        Schema::create('Announcement', function (Blueprint $table) {
            $table->id('AnnouncementId');
            $table->string('AnnouncementType');
            $table->string('AnnouncementTitle');
            $table->text('AnnouncementBody');
            $table->string('AttachmentType');
            $table->text('AttachmentImage');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('Announcement');
    }
};
