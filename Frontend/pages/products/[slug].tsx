import { useRouter } from "next/router";

const ProductPage: React.FC = () => {
    const router = useRouter();
    const { slug } = router.query;

    return (
        <div className="">

        </div>
  );
};

export default ProductPage;
