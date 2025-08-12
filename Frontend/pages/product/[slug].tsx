import { useRouter } from "next/router";
import { TestProducts } from "@/constants";
import ProductDetailsPage from "@/components/product/productDetails";

interface ProductDetailsPageProps {
  TestProduct?: {
    id: number;
    slug: string;
    name: string;
    description: string;
    price: number;
    image: string;
    thumbnails: string[];
    keyFeatures?: string[];
  };
}

const ProductPage: React.FC<ProductDetailsPageProps> = () => {
  const router = useRouter();
  const { slug } = router.query;

  const TestProduct = TestProducts.find((p) => p.slug === String(slug));

  if (!TestProduct) {
    return <p className="p-4">Product not found.</p>;
  }

  return (
    <div>
      <ProductDetailsPage TestProduct={TestProduct} />
    </div>
  );
};

export default ProductPage;
