"use client";

import React, { useState, useMemo, useCallback, useRef, useEffect } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { Product, ProductQueryParams } from "@/types";
import { formatCurrency, formatDate } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search, ArrowUpDown, Eye, ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";

interface DataTableProps {
  products: Product[];
  loading: boolean;
  total: number;
  page: number;
  totalPages: number;
  onParamsChange: (params: ProductQueryParams) => void;
  currentParams: ProductQueryParams;
}

export function DataTable({
  products,
  loading,
  total,
  page,
  totalPages,
  onParamsChange,
  currentParams,
}: DataTableProps) {
  const [search, setSearch] = useState(currentParams.search || "");
  const [category, setCategory] = useState(currentParams.category || "all");
  const [sortBy, setSortBy] = useState<"name" | "price" | "created_at" | "rating" | "stock">(
    (currentParams.sort_by as any) || "created_at"
  );
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">(
    currentParams.sort_order || "desc"
  );

  // Client-side filtering and sorting for instant response
  const filteredAndSortedProducts = useMemo(() => {
    let filtered = [...products];

    // Client-side search
    if (search) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(
        (p) =>
          p.name.toLowerCase().includes(searchLower) ||
          p.description.toLowerCase().includes(searchLower) ||
          p.sku.toLowerCase().includes(searchLower)
      );
    }

    // Client-side category filter
    if (category && category !== "all") {
      filtered = filtered.filter((p) => p.category === category);
    }

    // Client-side sorting
    filtered.sort((a, b) => {
      let aVal: any = a[sortBy];
      let bVal: any = b[sortBy];

      if (sortBy === "price" || sortBy === "rating" || sortBy === "stock") {
        aVal = aVal || 0;
        bVal = bVal || 0;
      } else if (sortBy === "name") {
        aVal = (aVal || "").toLowerCase();
        bVal = (bVal || "").toLowerCase();
      } else if (sortBy === "created_at") {
        aVal = new Date(aVal).getTime();
        bVal = new Date(bVal).getTime();
      }

      if (sortOrder === "asc") {
        return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      } else {
        return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
      }
    });

    return filtered;
  }, [products, search, category, sortBy, sortOrder]);

  // Get unique categories
  const categories = useMemo(() => {
    const cats = new Set(products.map((p) => p.category).filter(Boolean));
    return Array.from(cats).sort();
  }, [products]);

  // Virtual scrolling setup
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: filteredAndSortedProducts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
    overscan: 10,
  });

  // Sync category state with currentParams
  useEffect(() => {
    const normalizedCategory = currentParams.category || "all";
    if (category !== normalizedCategory) {
      setCategory(normalizedCategory);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentParams.category]);

  // Debounced search effect
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      onParamsChange({ ...currentParams, search: search || undefined, page: 1 });
    }, 300);
    return () => clearTimeout(timeoutId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search]); // Only trigger on search change to avoid loops

  const handleCategoryChange = useCallback(
    (value: string) => {
      setCategory(value); // Keep "all" in state for Select component
      // Convert "all" to undefined for API call
      const apiCategory = value === "all" ? undefined : value;
      onParamsChange({ ...currentParams, category: apiCategory, page: 1 });
    },
    [currentParams, onParamsChange]
  );

  const handleSortChange = useCallback(
    (field: "name" | "price" | "created_at" | "rating" | "stock") => {
      if (sortBy === field) {
        setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        onParamsChange({
          ...currentParams,
          sort_by: field,
          sort_order: sortOrder === "asc" ? "desc" : "asc",
        });
      } else {
        setSortBy(field);
        setSortOrder("desc");
        onParamsChange({
          ...currentParams,
          sort_by: field,
          sort_order: "desc",
        });
      }
    },
    [sortBy, sortOrder, currentParams, onParamsChange]
  );

  const handlePageChange = useCallback(
    (newPage: number) => {
      onParamsChange({ ...currentParams, page: newPage });
    },
    [currentParams, onParamsChange]
  );

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Products ({total.toLocaleString()} total)</span>
          <div className="text-sm font-normal text-muted-foreground">
            Showing {filteredAndSortedProducts.length} of {products.length} on this page
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={category} onValueChange={handleCategoryChange}>
            <SelectTrigger className="w-full sm:w-[200px]">
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Sort Controls */}
        <div className="flex flex-wrap gap-2">
          <Button
            variant={sortBy === "name" ? "default" : "outline"}
            size="sm"
            onClick={() => handleSortChange("name")}
          >
            Name
            {sortBy === "name" && (
              <ArrowUpDown className="ml-2 h-3 w-3" />
            )}
          </Button>
          <Button
            variant={sortBy === "price" ? "default" : "outline"}
            size="sm"
            onClick={() => handleSortChange("price")}
          >
            Price
            {sortBy === "price" && (
              <ArrowUpDown className="ml-2 h-3 w-3" />
            )}
          </Button>
          <Button
            variant={sortBy === "rating" ? "default" : "outline"}
            size="sm"
            onClick={() => handleSortChange("rating")}
          >
            Rating
            {sortBy === "rating" && (
              <ArrowUpDown className="ml-2 h-3 w-3" />
            )}
          </Button>
          <Button
            variant={sortBy === "stock" ? "default" : "outline"}
            size="sm"
            onClick={() => handleSortChange("stock")}
          >
            Stock
            {sortBy === "stock" && (
              <ArrowUpDown className="ml-2 h-3 w-3" />
            )}
          </Button>
          <Button
            variant={sortBy === "created_at" ? "default" : "outline"}
            size="sm"
            onClick={() => handleSortChange("created_at")}
          >
            Date
            {sortBy === "created_at" && (
              <ArrowUpDown className="ml-2 h-3 w-3" />
            )}
          </Button>
        </div>

        {/* Virtualized Table */}
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-center space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
              <p className="text-sm text-muted-foreground">Loading products...</p>
            </div>
          </div>
        ) : filteredAndSortedProducts.length === 0 ? (
          <div className="flex items-center justify-center h-96">
            <p className="text-muted-foreground">No products found</p>
          </div>
        ) : (
          <>
            <div
              ref={parentRef}
              className="h-[600px] overflow-auto border rounded-md"
            >
              <div
                style={{
                  height: `${virtualizer.getTotalSize()}px`,
                  width: "100%",
                  position: "relative",
                }}
              >
                {virtualizer.getVirtualItems().map((virtualRow) => {
                  const product = filteredAndSortedProducts[virtualRow.index];
                  return (
                    <div
                      key={virtualRow.key}
                      style={{
                        position: "absolute",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: `${virtualRow.size}px`,
                        transform: `translateY(${virtualRow.start}px)`,
                      }}
                      className="border-b"
                    >
                      <div className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-3">
                            <h3 className="font-semibold truncate">{product.name}</h3>
                            <Badge variant="outline">{product.category}</Badge>
                            {product.rating && (
                              <Badge variant="secondary">
                                ⭐ {product.rating.toFixed(1)}
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground truncate mt-1">
                            {product.description}
                          </p>
                          <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                            <span>SKU: {product.sku}</span>
                            <span>Stock: {product.stock}</span>
                            {product.brand && <span>Brand: {product.brand}</span>}
                          </div>
                        </div>
                        <div className="flex items-center gap-4 ml-4">
                          <div className="text-right">
                            <div className="font-semibold text-lg">
                              {formatCurrency(product.price)}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {formatDate(product.created_at)}
                            </div>
                          </div>
                          <Link href={`/products/${product._id}`}>
                            <Button variant="ghost" size="icon">
                              <Eye className="h-4 w-4" />
                            </Button>
                          </Link>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                  Page {page} of {totalPages}
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handlePageChange(page - 1)}
                    disabled={page === 1}
                  >
                    <ChevronLeft className="h-4 w-4" />
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handlePageChange(page + 1)}
                    disabled={page === totalPages}
                  >
                    Next
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}

