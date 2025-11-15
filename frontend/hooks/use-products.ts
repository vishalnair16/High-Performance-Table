import { useState, useEffect, useCallback } from "react";
import api from "@/lib/api";
import { Product, ProductListResponse, ProductQueryParams } from "@/types";

interface UseProductsReturn {
  products: Product[];
  loading: boolean;
  error: string | null;
  total: number;
  page: number;
  totalPages: number;
  fetchProducts: (params?: ProductQueryParams) => Promise<void>;
  refetch: () => Promise<void>;
}

export function useProducts(initialParams?: ProductQueryParams): UseProductsReturn {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(initialParams?.page || 1);
  const [totalPages, setTotalPages] = useState(0);
  const [currentParams, setCurrentParams] = useState<ProductQueryParams>(initialParams || {});

  const fetchProducts = useCallback(async (params?: ProductQueryParams) => {
    setLoading(true);
    setError(null);

    const queryParams = { ...currentParams, ...params };
    setCurrentParams(queryParams);

    try {
      const response = await api.get<ProductListResponse>("/api/v1/products", {
        params: {
          page: queryParams.page || 1,
          page_size: queryParams.page_size || 50,
          search: queryParams.search,
          category: queryParams.category,
          min_price: queryParams.min_price,
          max_price: queryParams.max_price,
          min_stock: queryParams.min_stock,
          sort_by: queryParams.sort_by || "created_at",
          sort_order: queryParams.sort_order || "desc",
          tags: queryParams.tags,
        },
      });

      setProducts(response.data.products);
      setTotal(response.data.total);
      setPage(response.data.page);
      setTotalPages(response.data.total_pages);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to fetch products";
      setError(errorMessage);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  }, [currentParams]);

  const refetch = useCallback(() => {
    return fetchProducts(currentParams);
  }, [fetchProducts, currentParams]);

  useEffect(() => {
    fetchProducts(initialParams);
  }, []);

  return {
    products,
    loading,
    error,
    total,
    page,
    totalPages,
    fetchProducts,
    refetch,
  };
}

