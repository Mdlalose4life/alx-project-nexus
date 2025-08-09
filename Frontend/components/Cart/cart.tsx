import HorizintalDevider from "../common/Dividers/Horizontal-devider";
import CartItem from "./cart/cartItem";
import CartPriceSumary from "./cart/cartPriceSumary";

const Cart: React.FC = () => {
  return (
    <div className="flex flex-col gap-5 w-full lg:w-[100%] p-2">
      <div className="flex flex-col gap-2">
        <span className="font-semibold text-2xl">Shopping Card</span>
        <HorizintalDevider color="bg-gray-300" thickness="h-[1px]" />       
      </div>
      <div className="flex flex-col lg:flex-row gap-6 w-full lg:w-[100%]">
        <CartItem/>
        <CartPriceSumary/>        
      </div>

    </div>
  );
};

export default Cart;