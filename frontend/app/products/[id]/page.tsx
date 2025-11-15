"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { Product } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatDate } from "@/lib/utils";
import { ArrowLeft, Package, DollarSign, Star, Box, Tag, Calendar } from "lucide-react";
import Link from "next/link";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!params.id || typeof params.id !== "string") {
        setError("Invalid product ID");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await api.get<Product>(`/api/v1/products/${params.id}`);
        setProduct(response.data);
        setError(null);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to load product";
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [params.id]);

  if (loading) {
    return (
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="flex items-center justify-center h-96">
            <div className="text-center space-y-2">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
              <p className="text-sm text-muted-foreground">Loading product...</p>
            </div>
          </div>
        </div>
      </main>
    );
  }

  if (error || !product) {
    return (
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <Card className="border-destructive">
            <CardContent className="pt-6">
              <p className="text-destructive mb-4">Error: {error || "Product not found"}</p>
              <Link href="/">
                <Button>Back to Products</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Link href="/">
          <Button variant="ghost" className="mb-6">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Products
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <CardTitle className="text-3xl mb-2">{product.name}</CardTitle>
                <CardDescription className="text-base">{product.description}</CardDescription>
              </div>
              <Badge variant="outline" className="ml-4">
                {product.category}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Price and Rating */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3 p-4 border rounded-lg">
                <DollarSign className="h-5 w-5 text-primary" />
                <div>
                  <div className="text-sm text-muted-foreground">Price</div>
                  <div className="text-2xl font-bold">{formatCurrency(product.price)}</div>
                </div>
              </div>
              {product.rating && (
                <div className="flex items-center gap-3 p-4 border rounded-lg">
                  <Star className="h-5 w-5 text-primary" />
                  <div>
                    <div className="text-sm text-muted-foreground">Rating</div>
                    <div className="text-2xl font-bold">
                      {product.rating.toFixed(1)} ⭐
                      {product.reviews_count && (
                        <span className="text-sm font-normal text-muted-foreground ml-2">
                          ({product.reviews_count} reviews)
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Stock and SKU */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3 p-4 border rounded-lg">
                <Box className="h-5 w-5 text-primary" />
                <div>
                  <div className="text-sm text-muted-foreground">Stock</div>
                  <div className="text-xl font-semibold">
                    {product.stock.toLocaleString()} units
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3 p-4 border rounded-lg">
                <Package className="h-5 w-5 text-primary" />
                <div>
                  <div className="text-sm text-muted-foreground">SKU</div>
                  <div className="text-xl font-semibold">{product.sku}</div>
                </div>
              </div>
            </div>

            {/* Brand */}
            {product.brand && (
              <div className="flex items-center gap-3 p-4 border rounded-lg">
                <Tag className="h-5 w-5 text-primary" />
                <div>
                  <div className="text-sm text-muted-foreground">Brand</div>
                  <div className="text-xl font-semibold">{product.brand}</div>
                </div>
              </div>
            )}

            {/* Tags */}
            {product.tags && product.tags.length > 0 && (
              <div>
                <div className="text-sm font-medium mb-2">Tags</div>
                <div className="flex flex-wrap gap-2">
                  {product.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <div className="text-sm text-muted-foreground">Created</div>
                  <div className="text-sm">{formatDate(product.created_at)}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <div className="text-sm text-muted-foreground">Last Updated</div>
                  <div className="text-sm">{formatDate(product.updated_at)}</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}

