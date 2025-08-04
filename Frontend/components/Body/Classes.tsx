import { BiCategory } from "react-icons/bi";
import { FaChevronDown } from "react-icons/fa";
import { CiShop, CiLocationOn } from "react-icons/ci";
import { IoIosPricetag } from "react-icons/io";

const Classes: React.FC = () => {
  return (
    <section className="w-[100%]">
      <div className="overflow-x-auto bg-[#d9d9d9] ">
        <div className="flex justify-between w-[100%] gap-3 px-4 py-2">
          <button className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
            <BiCategory size={20}/>
            Categories
            <FaChevronDown />
          </button>
          <button className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
            <CiShop size={20} />
            Shop
            <FaChevronDown />
          </button>
          <button className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
            <CiLocationOn size={20} />
            Location
            <FaChevronDown />
          </button>
          <button className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
            <IoIosPricetag size={20} />
            Prices
            <FaChevronDown />
          </button>
        </div>
      </div>
    </section>
  );
};

export default Classes;
