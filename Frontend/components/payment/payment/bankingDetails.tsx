import { useState } from "react";
import { HiOutlineCreditCard } from "react-icons/hi";

const BankingDetails: React.FC = () => {
  const [method, setMethod] = useState("card");

  return (
    <div className="bg-[#f1efff] rounded-3xl p-6 w-full max-w-xl">
      <label htmlFor="payment-method" className="block mb-2 font-semibold text-black">
        Payment Method
      </label>
      <div className="relative mb-4">
        <select
          id="payment-method"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          className="w-full rounded-xl border border-gray-400 bg-purple-50 text-gray-500 pl-12 pr-8 py-2 appearance-none focus:outline-none focus:ring-2 focus:ring-purple-300"
        >
          <option value="card">Card</option>
          <option value="paypal">PayPal</option>
          <option value="bank">Bank Transfer</option>
        </select>
        <HiOutlineCreditCard className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" size={20} />
        <svg
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 pointer-events-none"
          width="20"
          height="20"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          viewBox="0 0 24 24"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-6">
        <input
          type="text"
          placeholder="Card Number"
          className="border p-2 border-gray-300 rounded-lg bg-purple-50 h-12"
        />
        <input
          type="text"
          placeholder="CVV"
          className="border p-2 border-gray-300 rounded-lg bg-purple-50 h-12"
        />
      </div>

      <hr className="border-gray-300 mb-4" />

      <button
        type="submit"
        className="w-full bg-[#c3c1fb] rounded-full py-2 text-center font-medium text-black hover:bg-[#a3a1f8] transition"
      >
        Payment
      </button>
    </div>
  );
};

export default BankingDetails;