from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, and_, extract
from sqlalchemy.exc import NoResultFound
from config.settings import get_db, settings
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from app.utils.blog import generate_slug, generate_friendly_url, parse_friendly_url

import base64

router = APIRouter(prefix="/blog")
news_router = APIRouter(prefix="/news")

@router.get("/", response_model=list[BlogResponse])
async def list_published(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Blog).where(Blog.municipality_id.isnot(None)).order_by(desc(Blog.news_date)).limit(6)
    )
    return result.scalars().all()

@router.post("/", response_model=BlogResponse)
async def create_blog(data: BlogCreate, db: AsyncSession = Depends(get_db)):
    if data.password != settings.APP_BLOG_PASS:
        raise HTTPException(status_code=403, detail="Permission denied")

    result = await db.execute(select(func.max(Blog.id)))
    max_id = result.scalar() or 0
    
    blog_data = data.model_dump(exclude={"password"})
    blog = Blog(**blog_data)
    blog.id = max_id + 1
    
    # Generate slug if not provided
    if not blog.slug:
        blog.slug = generate_slug(blog.title)
    
    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog

@router.get("/{id}", response_model=BlogResponse)
async def get_blog(id: int, db: AsyncSession = Depends(get_db)):
    blog = await db.get(Blog, id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{id}", response_model=BlogResponse)
async def update_blog(id: int, data: BlogUpdate, db: AsyncSession = Depends(get_db)):
    if data.password != settings.APP_BLOG_PASS:
        raise HTTPException(status_code=403, detail="Permission denied")

    blog = await db.get(Blog, id)
    if not blog:
        raise HTTPException(status_code=400, detail="Blog not found")

    for field, value in data.model_dump(exclude={"password"}).items():
        setattr(blog, field, value)

    # Update slug if title changed
    if hasattr(data, 'title') and data.title:
        if not data.slug:
            blog.slug = generate_slug(data.title)

    await db.commit()
    await db.refresh(blog)
    return blog

@router.delete("/{id}/{password}", response_model=int)
async def delete_blog(id: int, password: str, db: AsyncSession = Depends(get_db)):
    try:
        decoded = base64.b64decode(password).decode()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid password encoding")

    if decoded != settings.APP_BLOG_PASS:
        raise HTTPException(status_code=403, detail="Permission denied")

    blog = await db.get(Blog, id)
    if not blog:
        raise HTTPException(status_code=400, detail="Blog not found")

    await db.delete(blog)
    await db.commit()
    return 1

@router.get("/user/{key}", response_model=list[BlogResponse])
async def get_all_blogs(key: str, db: AsyncSession = Depends(get_db)):
    if key != settings.APP_BLOG_PASS:
        raise HTTPException(status_code=403, detail="Permission denied")

    result = await db.execute(select(Blog).order_by(desc(Blog.id)))
    return result.scalars().all()

# News endpoints for public consumption
@news_router.get("/", response_model=list[BlogResponse])
async def list_news(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=50, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    List published news articles with pagination.
    """
    offset = (page - 1) * per_page
    
    result = await db.execute(
        select(Blog)
        .where(Blog.municipality_id.isnot(None))
        .order_by(desc(Blog.news_date))
        .offset(offset)
        .limit(per_page)
    )
    return result.scalars().all()

@news_router.get("/{year}/{month}/{slug}", response_model=BlogResponse)
async def get_news_by_friendly_url(
    year: int, 
    month: int, 
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a news article by its friendly URL.
    Format: /news/2025/06/apple-explica-por-que-se-ha-retrasado-siri-apple-intelligence
    """
    result = await db.execute(
        select(Blog)
        .where(
            and_(
                Blog.municipality_id.isnot(None),
                Blog.slug == slug,
                extract('year', Blog.news_date) == year,
                extract('month', Blog.news_date) == month
            )
        )
    )
    
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="News article not found")
    
    return blog

@news_router.get("/{id}", response_model=BlogResponse)
async def get_news_by_id(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a news article by its ID (fallback for existing links).
    """
    result = await db.execute(
        select(Blog).where(and_(Blog.id == id, Blog.municipality_id.isnot(None)))
    )
    
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail="News article not found")
    
    return blog
