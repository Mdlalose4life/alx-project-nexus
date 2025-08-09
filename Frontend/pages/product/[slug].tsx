import { useRouter } from "next/router";
import { TestProducts } from "@/constants";
import ProductDetailsPage from "@/components/product/productDetails";

const ProductPage: React.FC = () => {
    const router = useRouter();
    const { slug } = router.query;

    const TestProduct = TestProducts.find((p) => p.slug === slug);

    if (!TestProducts) {
      return <p className="p-4"> Loading Products...</p>
    }

    console.log(TestProduct)

    return (
        <div className="">
          <ProductDetailsPage TestProduct={TestProduct}/>
        </div>
  );
};

export default ProductPage;
