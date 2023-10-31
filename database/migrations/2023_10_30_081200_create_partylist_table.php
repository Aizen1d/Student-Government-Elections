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
        Schema::create('PartyList', function (Blueprint $table) {
            $table->id('PartyListId');

            $table->unsignedBigInteger('ElectionId');
            $table->foreign('ElectionId')->references('ElectionId')->on('Election');

            $table->string('PartyListName');
            $table->text('Description');
            $table->text('Platforms');
            $table->string('EmailAddress');
            $table->string('CellphoneNumber');
            $table->text('Vision');
            $table->text('Mission');
            $table->string('ImageAttachment')->nullable();
            $table->string('VideoAttachment')->nullable();
            $table->string('Status');

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('PartyList');
    }
};
