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
        Schema::create('InsertDataQueues', function (Blueprint $table) {
            $table->id('QueueId');
            $table->string('QueueName');
            $table->unsignedBigInteger('ToEmailTotal');
            $table->unsignedBigInteger('EmailSent');
            $table->unsignedBigInteger('EmailFailed');
            $table->string('Status');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('InsertDataQueues');
    }
};
