<?php

namespace App\Models;

use Illuminate\Auth\Authenticatable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Tymon\JWTAuth\Contracts\JWTSubject; 

class Comelec extends Model implements JWTSubject, AuthenticatableContract
{
    use HasFactory, Authenticatable;

    protected $table = "SGEComelec";
    protected $primaryKey = 'ComelecId';
    protected $fillable = ['StudentNumber', 'ComelecPassword', 'Position'];

    public function getAuthPassword()
    {
        return $this->ComelecPassword;
    }

    public function getStudentByStudentNumber()
    {
        return $this->belongsTo(Student::class, 'StudentNumber', 'StudentNumber');
    }

    /**
     * Get the identifier that will be stored in the subject claim of the JWT.
     *
     * @return mixed
     */
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
