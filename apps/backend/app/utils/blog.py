import re
import unicodedata
from datetime import date


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a blog title.
    
    Args:
        title: The blog post title
        
    Returns:
        A URL-friendly slug
    """
    # Convert to lowercase
    slug = title.lower()
    
    # Replace accented characters with their ASCII equivalents
    slug = unicodedata.normalize('NFKD', slug)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def generate_friendly_url(title: str, news_date: date) -> str:
    """
    Generate a friendly URL path for a blog post.
    Format: /news/YYYY/MM/slug

    Args:
        title: The blog post title
        news_date: The publication date

    Returns:
        A friendly URL path
    """
    slug = generate_slug(title)
    year = news_date.year
    month = f"{news_date.month:02d}"

    return f"/news/{year}/{month}/{slug}"


def parse_friendly_url(url_path: str) -> tuple[int, int, str]:
    """
    Parse a friendly URL to extract year, month, and slug.
    
    Args:
        url_path: The URL path in format /news/YYYY/MM/slug
        
    Returns:
        Tuple of (year, month, slug)
        
    Raises:
        ValueError: If URL format is invalid
    """
    # Remove leading/trailing slashes and split
    parts = url_path.strip('/').split('/')
    
    if len(parts) != 4 or parts[0] != 'news':
        raise ValueError("Invalid URL format. Expected /news/YYYY/MM/slug")
    
    try:
        year = int(parts[1])
        month = int(parts[2])
        slug = parts[3]
        
        if year < 1900 or year > 3000:
            raise ValueError("Invalid year")
        if month < 1 or month > 12:
            raise ValueError("Invalid month")
            
        return year, month, slug
    except ValueError as e:
        raise ValueError(f"Invalid URL format: {e}")
