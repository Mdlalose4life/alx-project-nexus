import { PiShoppingCartLight } from "react-icons/pi";

interface CartProp {
  activeView: string | null;
  setActiveView: (view: "Cart" | "Profile" | "More" | null) => void;
}

const Cart: React.FC<CartProp> = ({ activeView, setActiveView }) => {
  const cartItemCount = 1;
  const isOpen = activeView === "Cart";

  const toggleCart = () => {
    setActiveView(isOpen ? null : "Cart");
  };

  return (
    <div className="relative">
      <button
        onClick={toggleCart}
        className="relative p-2 hover:scale-105 transform transition duration-300 cursor-pointer"
      >
        <PiShoppingCartLight size={30} />

        {cartItemCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-600 text-white text-xs font-semibold w-4 h-5 flex items-center justify-center rounded-full shadow-md">
            {cartItemCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-[150px] bg-[#EDECFE] text-black p-3 rounded-xl shadow-xl z-20">
          <div className="flex items-start gap-2 mb-2">
            <img
              src="/Images/productA.webp"
              alt="Cart Product"
              className="h-[30px] w-[40px] object-cover rounded"
            />
            <div>
              <h3 className="text-sm lg:text-md font-semibold">LG OLED</h3>
              <span className="text-sm lg:text-md ">R 1200</span>
            </div>
          </div>
          <button className="bg-[#D5D3FD] rounded-2xl py-2 w-full text-sm font-medium hover:bg-[#c2c0f5] transition-colors lg:text-md">
            Checkout
          </button>
        </div>
      )}
    </div>
  );
};

export default Cart;
