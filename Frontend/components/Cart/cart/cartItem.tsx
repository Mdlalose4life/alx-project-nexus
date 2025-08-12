import { FiTrash2 } from "react-icons/fi";
import { FaMinus, FaPlus } from "react-icons/fa6";
import { MdStore } from "react-icons/md";
import Image from "next/image";

const CartItem: React.FC= () => {
  return (
        <div className="flex flex-col p-6 bg-[#f1efff] rounded-3xl lg:w-[60%]">
      <div className="flex items-start gap-4">
          <div className="w-30 h-20 rounded-xl overflow-hidden bg-white p-1 flex items-center justify-center">
          <Image src="/images/productE.webp" alt="Alt Text here" width={100} height={90} className="object-contain" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold lg:text-lg">LG OLED evo C3 4K Smart TV</h3>
          <p className="text-gray-600 text-md font-medium lg:text-lg">R 2 700</p>
        </div>

         <div className="flex items-center bg-gray-200 rounded-full px-2 py-1">
          <button className="p-1">
            <FaMinus size={12} />
          </button>
          <span className="mx-2 font-medium lg:text-2xl">1</span>
          <button className="p-1">
            <FaPlus size={12} />
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-gray-300 mt-3 pt-2">
        <div className="flex items-center gap-1 text-sm text-gray-800 font-medium lg:text-lg">
          <MdStore />
          Evetech
        </div>
        <button className="flex items-center text-red-500 gap-1 text-sm font-medium lg:text-lg">
          <FiTrash2 size={16} />
          Remove Item
        </button>
      </div>
    </div>
  );
};

export default CartItem;
