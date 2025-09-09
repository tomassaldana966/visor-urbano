import os
import tempfile
import logging
import re
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.business_signatures import BusinessSignature
from app.models.user import UserModel
from app.schemas.business_signature import BusinessSignatureResponseSchema
from config.settings import get_session
from config.security import get_current_user
from datetime import datetime, timezone
import shutil
import subprocess
import secrets

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.cer', '.key'}
ALLOWED_MIME_TYPES = {
    'application/x-x509-ca-cert',
    'application/x-x509-user-cert', 
    'application/pkcs8',
    'application/octet-stream'
}
SIGNATURES_BASE_DIR = os.getenv('SIGNATURES_BASE_DIR', 'business_license_signatures')
CURP_PATTERN = re.compile(r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$')

router = APIRouter(
    prefix="/electronic_signature"    
)

def validate_curp(curp: str) -> bool:
    if not curp or len(curp) != 18:
        return False
    return bool(CURP_PATTERN.match(curp))

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    if not filename:
        return False
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions

def validate_file_content(file_content: bytes, expected_ext: str) -> bool:
    try:
        if expected_ext == '.cer':
            return file_content.startswith(b'\x30\x82')
        elif expected_ext == '.key':
            return (file_content.startswith(b'\x30\x82') or 
                   b'-----BEGIN' in file_content)
        return False
    except Exception:
        return False

def validate_file_size(file: UploadFile, max_size: int) -> bool:
    try:
        file.file.seek(0)
        file_size = 0
        chunk_size = 8192
        while True:
            chunk = file.file.read(chunk_size)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > max_size:
                file.file.seek(0)
                return False
        file.file.seek(0)
        return True
    except Exception as e:
        logger.error(f"Error while validating file size: {e}")
        try:
            file.file.seek(0)
        except:
            pass
        return False

def secure_filename(filename: str) -> str:
    if not filename:
        return "unknown"
    safe_name = Path(filename).name
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in '._-')
    if len(safe_name) > 100:
        if '.' in safe_name:
            name, ext = safe_name.rsplit('.', 1)
            max_name_length = 100 - len(ext) - 1
            safe_name = name[:max_name_length] + '.' + ext
        else:
            safe_name = safe_name[:100]
    return safe_name

def create_secure_temp_dir() -> str:
    temp_dir = tempfile.mkdtemp(
        prefix="business_sig_",
        dir=tempfile.gettempdir()
    )
    os.chmod(temp_dir, 0o700)
    return temp_dir

async def cleanup_files(*file_paths: str) -> None:
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)
                else:
                    os.remove(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup {file_path}: {e}")

def run_openssl_command(cmd: list, capture_output: bool = False, 
                       input_data: str = None) -> subprocess.CompletedProcess:
    if not cmd or not isinstance(cmd, list):
        raise ValueError("Invalid command format")
    if cmd[0] != 'openssl':
        raise ValueError("Only OpenSSL commands are allowed")
    try:
        logger.info(f"Running OpenSSL command: {' '.join(cmd[:3])}...")
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            timeout=30,
            check=False,
            input=input_data,
            env={'PATH': os.environ.get('PATH', ''), 'LC_ALL': 'C'}
        )
        if result.returncode != 0:
            logger.error(f"OpenSSL command failed with code {result.returncode}")
        return result
    except subprocess.TimeoutExpired:
        logger.error("OpenSSL command timed out")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Certificate processing timed out"
        )
    except Exception as e:
        logger.error(f"OpenSSL command failed: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Certificate processing failed"
        )

async def validate_signature_input(curp: str, file_cer: UploadFile, file_key: UploadFile, current_user: UserModel) -> tuple:
    if not validate_curp(curp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid CURP format"
        )
    
    if not validate_file_extension(file_cer.filename, {'.cer'}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate file must have .cer extension"
        )
    
    if not validate_file_extension(file_key.filename, {'.key'}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Private key file must have .key extension"
        )
    
    if not validate_file_size(file_cer, MAX_FILE_SIZE):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Certificate file too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    if not validate_file_size(file_key, MAX_FILE_SIZE):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Private key file too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    user_id = current_user.id
    role_id = current_user.user_roles.id if current_user.user_roles else None
    if role_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have a role assigned to create electronic signatures"
        )
    
    return user_id, role_id


async def prepare_signature_files(file_cer: UploadFile, file_key: UploadFile, chain: str, temp_dir: str) -> tuple:
    cer_content = await file_cer.read()
    key_content = await file_key.read()
    
    if not validate_file_content(cer_content, '.cer'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid certificate file format"
        )
    
    if not validate_file_content(key_content, '.key'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid private key file format"
        )
    
    cer_filename = secure_filename(file_cer.filename)
    key_filename = secure_filename(file_key.filename)
    
    cer_path = os.path.join(temp_dir, f"cert_{secrets.token_hex(8)}.cer")
    key_path = os.path.join(temp_dir, f"key_{secrets.token_hex(8)}.key")
    chain_path = os.path.join(temp_dir, f"chain_{secrets.token_hex(8)}.txt")
    
    with open(cer_path, "wb") as f:
        f.write(cer_content)
    os.chmod(cer_path, 0o600)
    
    with open(key_path, "wb") as f:
        f.write(key_content)
    os.chmod(key_path, 0o600)
    
    with open(chain_path, "w") as f:
        f.write(chain)
    os.chmod(chain_path, 0o600)
    
    return cer_path, key_path, chain_path, cer_filename, key_filename


async def convert_certificates_to_pem(cer_path: str, key_path: str, password: str, temp_dir: str) -> tuple:
    pem_cer_path = os.path.join(temp_dir, f"cert_{secrets.token_hex(8)}.pem")
    cert_convert_result = run_openssl_command([
        "openssl", "x509", "-in", cer_path, "-out", pem_cer_path,
        "-inform", "DER", "-outform", "PEM"
    ], capture_output=True)
    
    if cert_convert_result.returncode != 0:
        logger.error("Certificate conversion failed")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid certificate file format"
        )
    
    pem_key_path = os.path.join(temp_dir, f"key_{secrets.token_hex(8)}.pem")
    key_convert_result = run_openssl_command([
        "openssl", "pkcs8", "-inform", "DER", "-in", key_path,
        "-out", pem_key_path, "-passin", f"pass:{password}"
    ], capture_output=True)
    
    if key_convert_result.returncode != 0:
        logger.warning("Private key conversion failed - invalid password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid private key password"
        )
    
    return pem_cer_path, pem_key_path


async def generate_digital_signature(pem_cer_path: str, chain_path: str) -> str:
    hash_result = run_openssl_command([
        "openssl", "dgst", "-sha256", pem_cer_path, chain_path
    ], capture_output=True)
    
    if hash_result.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create hash"
        )
    
    encode_result = run_openssl_command([
        "openssl", "enc", "-base64", "-A"
    ], capture_output=True, input_data=hash_result.stdout)
    
    if encode_result.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to encode signature"
        )
    
    signed_hash = encode_result.stdout.strip()
    if not signed_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Empty signature generated"
        )
    
    return signed_hash


async def create_signature_record(
    procedure_id: int, user_id: int, role_id: int, chain: str, 
    signed_hash: str, curp: str, procedure_part: str, 
    cer_filename: str, key_filename: str, db: AsyncSession
) -> BusinessSignature:
    response_data = {
        "signed_hash": signed_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "curp": curp.upper(),
        "procedure_id": procedure_id,
        "procedure_part": procedure_part,
        "cert_filename": cer_filename,
        "key_filename": key_filename
    }
    
    signature_record = BusinessSignature(
        procedure_id=procedure_id,
        user_id=user_id,
        role=role_id,
        hash_to_sign=chain,
        signed_hash=signed_hash,
        response=response_data
    )
    
    db.add(signature_record)
    await db.commit()
    await db.refresh(signature_record)
    
    return signature_record


@router.get("/", response_model=List[BusinessSignatureResponseSchema])
async def get_business_signatures(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    procedure_id: Optional[int] = Query(None, description="Filter by procedure ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        query = select(BusinessSignature).where(BusinessSignature.deleted_at.is_(None))
        if procedure_id:
            query = query.where(BusinessSignature.procedure_id == procedure_id)
        if user_id:
            query = query.where(BusinessSignature.user_id == user_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        signatures = result.scalars().all()
        logger.info(f"Retrieved {len(signatures)} business signatures for user {current_user.id}")
        return signatures
    except Exception as e:
        logger.error(f"Error retrieving business signatures: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving business signatures"
        )

@router.get("/{signature_id}", response_model=BusinessSignatureResponseSchema)
async def get_business_signature(
    signature_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        query = select(BusinessSignature).where(
            BusinessSignature.id == signature_id,
            BusinessSignature.deleted_at.is_(None)
        )
        result = await db.execute(query)
        signature = result.scalar_one_or_none()
        if not signature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business signature not found"
            )
        logger.info(f"Retrieved business signature {signature_id} for user {current_user.id}")
        return signature
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving business signature {signature_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving business signature"
        )

@router.post("/", response_model=BusinessSignatureResponseSchema)
async def handle_electronic_signature(
    password: str = Form(..., min_length=8, max_length=100),
    chain: str = Form(..., min_length=1, max_length=10000),
    curp: str = Form(..., min_length=18, max_length=18),
    procedure_id: int = Form(..., gt=0),
    procedure_part: str = Form(..., min_length=1, max_length=100),
    file_cer: UploadFile = File(...),
    file_key: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    temp_dir = None
    try:
        user_id, role_id = await validate_signature_input(curp, file_cer, file_key, current_user)
        temp_dir = create_secure_temp_dir()
        cer_path, key_path, chain_path, cer_filename, key_filename = await prepare_signature_files(
            file_cer, file_key, chain, temp_dir
        )
        pem_cer_path, pem_key_path = await convert_certificates_to_pem(
            cer_path, key_path, password, temp_dir
        )
        signed_hash = await generate_digital_signature(pem_cer_path, chain_path)
        signature_record = await create_signature_record(
            procedure_id, user_id, role_id, chain, signed_hash, 
            curp, procedure_part, cer_filename, key_filename, db
        )
        logger.info(f"Electronic signature created successfully for user {user_id}, procedure {procedure_id}")
        return signature_record
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in electronic signature: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred during signature processing"
        )
    finally:
        if temp_dir:
            await cleanup_files(temp_dir)
