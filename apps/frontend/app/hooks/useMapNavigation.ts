import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router';

export function useMapNavigation(
  mapLoadingDelay = 1000,
  postNavigationDelay = 500
) {
  const [isMapLoading, setIsMapLoading] = useState(false);
  const navigate = useNavigate();

  const navigateToMap = useCallback(() => {
    setIsMapLoading(true);

    // Simulate map loading time (adjustable via parameters)
    setTimeout(() => {
      navigate('/map');
      // Keep loading state for a bit after navigation to account for component mounting
      setTimeout(() => {
        setIsMapLoading(false);
      }, postNavigationDelay);
    }, mapLoadingDelay);
  }, [navigate, mapLoadingDelay, postNavigationDelay]);

  const closeMapLoading = useCallback(() => {
    setIsMapLoading(false);
  }, []);

  return {
    isMapLoading,
    navigateToMap,
    closeMapLoading,
  };
}
