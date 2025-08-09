import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";
import Link from "next/link";

const CartPriceSumary: React.FC = () => {
  return (
    <div className="border border-[#EDECFE] bg-[#EDECFE] rounded-3xl p-4 lg:w-[40%]">
      <div className="flex flex-row lg:flex-col font-medium">
        <span className="font-semibold lg:text-lg">Order Summary</span>
      </div>
      <div className="flex flex-row justify-between p-3 font-medium lg:text-lg">
        <div>Items</div>
        <div>
          <span className="font-semibold text-gray-500 lg:text-lg">R 7 500</span>
          </div>
      </div>
      <HorizintalDevider color="bg-gray-100" thickness="h-[1px]"/>
      <div className="flex flex-row justify-between p-3 font-medium lg:text-lg">
        <div>Subtotal</div>
        <span className="font-semibold text-gray-500 lg:text-lg">R7 500</span>
      </div>
      <Link href="/PaymentPage">
        <div className="flex justify-center">
          <button className="bg-[#D5D3FD] rounded-4xl py-1 px-5 font-semibold lg:text-lg">Checkout</button>
      </div>
      </Link>
    </div>
  );
};

export default CartPriceSumary;