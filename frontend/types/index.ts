export interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  stock: number;
  sku: string;
  brand?: string;
  rating?: number;
  reviews_count?: number;
  tags?: string[];
  created_at: string;
  updated_at: string;
}

export interface ProductListResponse {
  products: Product[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProductQueryParams {
  page?: number;
  page_size?: number;
  search?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  min_stock?: number;
  sort_by?: "name" | "price" | "created_at" | "rating" | "stock";
  sort_order?: "asc" | "desc";
  tags?: string[];
}

export interface ProductStats {
  total_products: number;
  total_stock: number;
  avg_price: number;
  min_price: number;
  max_price: number;
  avg_rating: number;
}

