import pytest
from datetime import date
from app.utils.blog import generate_slug, generate_friendly_url, parse_friendly_url


class TestBlogUtils:
    """Test cases for blog utility functions."""

    class TestGenerateSlug:
        """Test cases for generate_slug function."""

        def test_basic_slug_generation(self):
            """Test basic slug generation."""
            result = generate_slug("Hello World")
            assert result == "hello-world"

        def test_slug_with_special_characters(self):
            """Test slug generation with special characters."""
            result = generate_slug("Hello, World! How are you?")
            assert result == "hello-world-how-are-you"

        def test_slug_with_accented_characters(self):
            """Test slug generation with accented characters."""
            result = generate_slug("Niño José María")
            assert result == "nino-jose-maria"

        def test_slug_with_numbers(self):
            """Test slug generation with numbers."""
            result = generate_slug("Article 123: The Beginning")
            assert result == "article-123-the-beginning"

        def test_slug_with_multiple_spaces(self):
            """Test slug generation with multiple spaces."""
            result = generate_slug("Hello    World   Test")
            assert result == "hello-world-test"

        def test_slug_with_hyphens(self):
            """Test slug generation with existing hyphens."""
            result = generate_slug("Pre-existing-hyphens Test")
            assert result == "pre-existing-hyphens-test"

        def test_slug_with_underscores(self):
            """Test slug generation with underscores."""
            result = generate_slug("Test_with_underscores")
            assert result == "test_with_underscores"

        def test_slug_empty_string(self):
            """Test slug generation with empty string."""
            result = generate_slug("")
            assert result == ""

        def test_slug_only_special_characters(self):
            """Test slug generation with only special characters."""
            result = generate_slug("!@#$%^&*()")
            assert result == ""

        def test_slug_leading_trailing_spaces(self):
            """Test slug generation with leading/trailing spaces."""
            result = generate_slug("  Hello World  ")
            assert result == "hello-world"

        def test_slug_leading_trailing_hyphens(self):
            """Test slug generation that would create leading/trailing hyphens."""
            result = generate_slug("!Hello World!")
            assert result == "hello-world"

        def test_slug_unicode_characters(self):
            """Test slug generation with various unicode characters."""
            result = generate_slug("Café naïve résumé")
            assert result == "cafe-naive-resume"

        def test_slug_mixed_case(self):
            """Test slug generation with mixed case."""
            result = generate_slug("ThIs Is A TeSt")
            assert result == "this-is-a-test"

    class TestGenerateFriendlyUrl:
        """Test cases for generate_friendly_url function."""

        def test_basic_friendly_url(self):
            """Test basic friendly URL generation."""
            title = "My Blog Post"
            news_date = date(2025, 6, 14)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2025/06/my-blog-post"

        def test_friendly_url_single_digit_month(self):
            """Test friendly URL generation with single digit month."""
            title = "January Post"
            news_date = date(2025, 1, 15)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2025/01/january-post"

        def test_friendly_url_december(self):
            """Test friendly URL generation with December."""
            title = "Year End Review"
            news_date = date(2024, 12, 31)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2024/12/year-end-review"

        def test_friendly_url_complex_title(self):
            """Test friendly URL generation with complex title."""
            title = "Breaking News: Major Update & Important Changes!"
            news_date = date(2025, 3, 22)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2025/03/breaking-news-major-update-important-changes"

        def test_friendly_url_accented_title(self):
            """Test friendly URL generation with accented characters."""
            title = "Información Importante para la Población"
            news_date = date(2025, 8, 5)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2025/08/informacion-importante-para-la-poblacion"

        def test_friendly_url_leap_year(self):
            """Test friendly URL generation with leap year date."""
            title = "Leap Year Special"
            news_date = date(2024, 2, 29)
            result = generate_friendly_url(title, news_date)
            assert result == "/news/2024/02/leap-year-special"

    class TestParseFriendlyUrl:
        """Test cases for parse_friendly_url function."""

        def test_basic_url_parsing(self):
            """Test basic URL parsing."""
            url = "/news/2025/06/my-blog-post"
            year, month, slug = parse_friendly_url(url)
            assert year == 2025
            assert month == 6
            assert slug == "my-blog-post"

        def test_url_parsing_without_leading_slash(self):
            """Test URL parsing without leading slash."""
            url = "news/2025/06/my-blog-post"
            year, month, slug = parse_friendly_url(url)
            assert year == 2025
            assert month == 6
            assert slug == "my-blog-post"

        def test_url_parsing_with_trailing_slash(self):
            """Test URL parsing with trailing slash."""
            url = "/news/2025/06/my-blog-post/"
            year, month, slug = parse_friendly_url(url)
            assert year == 2025
            assert month == 6
            assert slug == "my-blog-post"

        def test_url_parsing_single_digit_month(self):
            """Test URL parsing with single digit month."""
            url = "/news/2025/03/spring-update"
            year, month, slug = parse_friendly_url(url)
            assert year == 2025
            assert month == 3
            assert slug == "spring-update"

        def test_url_parsing_december(self):
            """Test URL parsing with December."""
            url = "/news/2024/12/year-end-summary"
            year, month, slug = parse_friendly_url(url)
            assert year == 2024
            assert month == 12
            assert slug == "year-end-summary"

        def test_url_parsing_complex_slug(self):
            """Test URL parsing with complex slug."""
            url = "/news/2025/07/this-is-a-very-long-slug-with-many-words"
            year, month, slug = parse_friendly_url(url)
            assert year == 2025
            assert month == 7
            assert slug == "this-is-a-very-long-slug-with-many-words"

        def test_url_parsing_invalid_format_too_few_parts(self):
            """Test URL parsing with too few parts."""
            url = "/news/2025/06"
            with pytest.raises(ValueError, match="Invalid URL format"):
                parse_friendly_url(url)

        def test_url_parsing_invalid_format_too_many_parts(self):
            """Test URL parsing with too many parts."""
            url = "/news/2025/06/slug/extra"
            with pytest.raises(ValueError, match="Invalid URL format"):
                parse_friendly_url(url)

        def test_url_parsing_invalid_prefix(self):
            """Test URL parsing with invalid prefix."""
            url = "/blog/2025/06/my-post"
            with pytest.raises(ValueError, match="Invalid URL format"):
                parse_friendly_url(url)

        def test_url_parsing_invalid_year(self):
            """Test URL parsing with invalid year."""
            url = "/news/abcd/06/my-post"
            with pytest.raises(ValueError, match="Invalid URL format"):
                parse_friendly_url(url)

        def test_url_parsing_invalid_month(self):
            """Test URL parsing with invalid month."""
            url = "/news/2025/xy/my-post"
            with pytest.raises(ValueError, match="Invalid URL format"):
                parse_friendly_url(url)

        def test_url_parsing_year_out_of_range_low(self):
            """Test URL parsing with year out of range (too low)."""
            url = "/news/1800/06/old-post"
            with pytest.raises(ValueError, match="Invalid year"):
                parse_friendly_url(url)

        def test_url_parsing_year_out_of_range_high(self):
            """Test URL parsing with year out of range (too high)."""
            url = "/news/3500/06/future-post"
            with pytest.raises(ValueError, match="Invalid year"):
                parse_friendly_url(url)

        def test_url_parsing_month_out_of_range_low(self):
            """Test URL parsing with month out of range (too low)."""
            url = "/news/2025/00/invalid-month"
            with pytest.raises(ValueError, match="Invalid month"):
                parse_friendly_url(url)

        def test_url_parsing_month_out_of_range_high(self):
            """Test URL parsing with month out of range (too high)."""
            url = "/news/2025/13/invalid-month"
            with pytest.raises(ValueError, match="Invalid month"):
                parse_friendly_url(url)

        def test_url_parsing_edge_case_years(self):
            """Test URL parsing with edge case years."""
            # Test minimum valid year
            url = "/news/1900/01/early-post"
            year, month, slug = parse_friendly_url(url)
            assert year == 1900
            
            # Test maximum valid year
            url = "/news/3000/12/future-post"
            year, month, slug = parse_friendly_url(url)
            assert year == 3000

        def test_url_parsing_edge_case_months(self):
            """Test URL parsing with edge case months."""
            # Test January
            url = "/news/2025/01/january-post"
            year, month, slug = parse_friendly_url(url)
            assert month == 1
            
            # Test December
            url = "/news/2025/12/december-post"
            year, month, slug = parse_friendly_url(url)
            assert month == 12

    class TestIntegration:
        """Integration tests for blog utility functions."""

        def test_round_trip_basic(self):
            """Test generating URL and parsing it back."""
            original_title = "My Test Blog Post"
            original_date = date(2025, 6, 14)
            
            # Generate URL
            url = generate_friendly_url(original_title, original_date)
            
            # Parse it back
            year, month, slug = parse_friendly_url(url)
            
            assert year == original_date.year
            assert month == original_date.month
            assert slug == generate_slug(original_title)

        def test_round_trip_complex(self):
            """Test round trip with complex title."""
            original_title = "Breaking News: Important Update & Changes!"
            original_date = date(2025, 12, 31)
            
            url = generate_friendly_url(original_title, original_date)
            year, month, slug = parse_friendly_url(url)
            
            assert year == original_date.year
            assert month == original_date.month
            assert slug == generate_slug(original_title)

        def test_round_trip_accented(self):
            """Test round trip with accented characters."""
            original_title = "Información Especial: Noticias Importantes"
            original_date = date(2025, 3, 15)
            
            url = generate_friendly_url(original_title, original_date)
            year, month, slug = parse_friendly_url(url)
            
            assert year == original_date.year
            assert month == original_date.month
            assert slug == generate_slug(original_title)


if __name__ == "__main__":
    pytest.main([__file__])
