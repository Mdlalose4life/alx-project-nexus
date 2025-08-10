import Cart from "@/components/Cart/cart";
import { useState } from "react";

const CartPage = () => {
  const [quantity, setQuantity] = useState(1);

  const handleIncrease = () => setQuantity((prev) => prev + 1);
  const handleDecrease = () => setQuantity((prev) => Math.max(1, prev - 1));
  const handleRemove = () => alert("Remove item clicked");

  return (
    <main className="">
      <Cart
        // name="LG OLED evo C3 4K Smart TV"
        // price={7500}
        // image="/Images/productG.jpeg"
        // seller="Evetech"
        // quantity={quantity}
        // onIncrease={handleIncrease}
        // onDecrease={handleDecrease}
        // onRemove={handleRemove}
      />
    </main>
  );
};

export default CartPage;
