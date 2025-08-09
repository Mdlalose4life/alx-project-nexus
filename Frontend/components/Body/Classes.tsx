'use client'

import { BiCategory } from "react-icons/bi";
import { FaChevronDown } from "react-icons/fa";
import { CiShop, CiLocationOn } from "react-icons/ci";
import { IoIosPricetag } from "react-icons/io";

const Classes: React.FC = () => {
    
  const categories = async()=>{
     const data = await fetch('/api/v1/business-categories');
      if (!data.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await data.json();
      console.log("hello data", result);
  
  } 

  const businesses = async()=>{
    const data = await fetch('/api/v1/businesses');
      if (!data.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await data.json();
      console.log("hello data", result);
      return result;
  }




  return (
    <section className="w-[100%]">
      <div className="overflow-x-auto bg-[#d9d9d9] ">
        <div className="flex justify-between w-[100%] gap-3 px-4 py-2">
          <button onClick={()=>{categories()}} className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
            <BiCategory size={20}/>
            Categories
            <FaChevronDown />
          </button>
          <button onClick={()=> { businesses()}} className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[8px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454]">
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
