import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";

const CartPriceSumary: React.FC = () => {
  return (
    <div className="border border-[#EDECFE] bg-[#EDECFE] rounded-3xl p-4 lg:w-[40%]">
      <div className="flex flex-row lg:flex-col font-medium">
        <span className="font-semibold lg:text-2xl">Order Summary</span>
      </div>
      <div className="flex flex-row justify-between p-3 font-medium lg:text-2xl">
        <div>Items</div>
        <div>
          <span className="font-semibold text-gray-500 lg:text-2xl">R 7 500</span>
          </div>
      </div>
      <HorizintalDevider color="bg-gray-300" thickness="h-[1px]"/>
      <div className="flex flex-row justify-between p-3 font-medium lg:text-2xl">
        <div>Subtotal</div>
        <span className="font-semibold text-gray-500 lg:text-2xl">R7 500</span>
      </div>
      <div className="flex justify-center">
          <button className="bg-[#D5D3FD] rounded-4xl py-1 px-5 font-semibold lg:text-2xl">Checkout</button>
      </div>
    </div>
  );
};

export default CartPriceSumary;