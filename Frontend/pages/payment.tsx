import Cart from "@/components/Cart/cart";
import Payment from "@/components/payment/payment";
import { useState } from "react";

const PaymentPage = () => {
  const [quantity, setQuantity] = useState(1);

  const handleIncrease = () => setQuantity((prev) => prev + 1);
  const handleDecrease = () => setQuantity((prev) => Math.max(1, prev - 1));
  const handleRemove = () => alert("Remove item clicked");

  return (
    <main className="">
      <Payment/>
    </main>
  );
};
export default PaymentPage;
