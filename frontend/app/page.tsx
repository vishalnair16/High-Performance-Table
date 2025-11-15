"use client";

import { useState, useCallback } from "react";
import { useProducts } from "@/hooks/use-products";
import { DataTable } from "@/components/data-table";
import { ProductQueryParams } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Package, DollarSign, Star, Box } from "lucide-react";
import { useEffect } from "react";
import api from "@/lib/api";
import { ProductStats } from "@/types";

export default function Home() {
  const [params, setParams] = useState<ProductQueryParams>({
    page: 1,
    page_size: 50,
    sort_by: "created_at",
    sort_order: "desc",
  });
  const [stats, setStats] = useState<ProductStats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const { products, loading, error, total, page, totalPages, fetchProducts } =
    useProducts(params);

  const handleParamsChange = useCallback(
    (newParams: ProductQueryParams) => {
      setParams((prev) => ({ ...prev, ...newParams }));
      fetchProducts(newParams);
    },
    [fetchProducts]
  );

  useEffect(() => {
    // Fetch stats
    const loadStats = async () => {
      try {
        const response = await api.get<ProductStats>("/api/v1/products/stats/summary");
        setStats(response.data);
      } catch (err) {
        console.error("Failed to load stats:", err);
      } finally {
        setStatsLoading(false);
      }
    };
    loadStats();
  }, []);

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">High Performance Data Table</h1>
          <p className="text-muted-foreground">
            Efficiently browse and manage 100,000+ products with instant search and filtering
          </p>
        </div>

        {/* Stats Cards */}
        {!statsLoading && stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Products</CardTitle>
                <Package className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_products.toLocaleString()}</div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Average Price</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  ${stats.avg_price.toFixed(2)}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Average Rating</CardTitle>
                <Star className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.avg_rating.toFixed(1)} ⭐
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Stock</CardTitle>
                <Box className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total_stock.toLocaleString()}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="mb-8 border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive">Error: {error}</p>
            </CardContent>
          </Card>
        )}

        {/* Data Table */}
        <DataTable
          products={products}
          loading={loading}
          total={total}
          page={page}
          totalPages={totalPages}
          onParamsChange={handleParamsChange}
          currentParams={params}
        />
      </div>
    </main>
  );
}

