<?php

namespace App\Models;

use Illuminate\Auth\Authenticatable;
use Tymon\JWTAuth\Contracts\JWTSubject; 
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;

class StudentPassword extends Model implements JWTSubject, AuthenticatableContract
{
    use HasFactory, Authenticatable;

    protected $table = "StudentPassword";
    protected $primaryKey = 'StudentPasswordId';
    protected $fillable = ['StudentNumber', 'Password'];

    public function getAuthPassword()
    {
        return $this->Password;
    }

    public function getJWTIdentifier()
    {
        return $this->getKey();
    }

    /**
     * Return a key value array, containing any custom claims to be added to the JWT.
     *
     * @return array
     */
    public function getJWTCustomClaims()
    {
        return [];
    }
}
