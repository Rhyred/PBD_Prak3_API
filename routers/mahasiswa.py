from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from database import get_db

# Router khusus Mahasiswa
router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])

# Model Validasi (Pydantic)
class MahasiswaInput(BaseModel):
    nim: str = Field(..., min_length=4, max_length=10)
    nama: str = Field(..., min_length=3)
    email: EmailStr
    id_prodi: int

# Endpoint GET (Dengan JOIN)
@router.get("/")
def get_semua_mahasiswa():
    db = get_db()
    cursor = db.cursor(dictionary=True) # dictionary=True mereturn JSON object
    
    sql = """
    SELECT m.nim, m.nama, p.nama_prodi
    FROM mahasiswa m
    JOIN prodi p ON m.id_prodi = p.id_prodi
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    
    return {"data": result}

# Endpoint POST & Parameterized Query
@router.post("/", status_code=201)
def tambah_mahasiswa(mhs: MahasiswaInput):
    db = get_db()
    cursor = db.cursor()
    
    sql = "INSERT INTO mahasiswa (nim, nama, email, id_prodi) VALUES (%s, %s, %s, %s)"
    val = (mhs.nim, mhs.nama, mhs.email, mhs.id_prodi)
    
    try:
        cursor.execute(sql, val)
        db.commit() # Saving permanen di database
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
        
    return {"message": "Great Saving GAGAH"}

# method Endpoint PUT (Update Data)
@router.put("/{nim}")
def update_mahasiswa(nim: str, mhs: MahasiswaInput):
    db = get_db()
    cursor = db.cursor()
    
    # Menggunakan query UPDATE dengan klausa WHERE agar aman[cite: 6]
    sql = "UPDATE mahasiswa SET nama = %s, email = %s, id_prodi = %s WHERE nim = %s"
    # Parameter nim diambil dari path URL, sedangkan data lainnya dari request body
    val = (mhs.nama, mhs.email, mhs.id_prodi, nim)
    
    try:
        cursor.execute(sql, val)
        # Cek apakah ada baris yang berhasil diupdate
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
        
    return {"message": f"Data mahasiswa dengan NIM {nim} berhasil diupdate"}


# method Endpoint DELETE (Hapus Data)
@router.delete("/{nim}")
def hapus_mahasiswa(nim: str):
    db = get_db()
    cursor = db.cursor()
    
    # Menggunakan query DELETE dengan klausa WHERE berdasarkan nim[cite: 6]
    sql = "DELETE FROM mahasiswa WHERE nim = %s"
    val = (nim,)
    
    try:
        cursor.execute(sql, val)
        # Cek apakah data benar-benar ada dan terhapus
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
        
    return {"message": f"Data mahasiswa dengan NIM {nim} berhasil dihapus"}