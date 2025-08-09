'use client'

import React, { forwardRef, useState } from "react";
import { BiCategory } from "react-icons/bi";
import { FaChevronDown } from "react-icons/fa";
import { CiShop, CiLocationOn } from "react-icons/ci";
import { IoIosPricetag } from "react-icons/io";
import { useMenu } from "@/store/MenuContext";

interface ClassesProps {
  setActivePanel: (panel: "left" | "right") => void;
  setActiveMenu: (menu: string) => void;
}

const Classes = forwardRef<HTMLDivElement, ClassesProps>(
  ({ setActivePanel, setActiveMenu }, ref) => {
    const { setActiveMenu: setMenuInContext } = useMenu();

    const handleClick = (menu: string, panel: "left" | "right") => {
      setActiveMenu(menu);
      setMenuInContext(menu as any);
      setActivePanel(panel);
    };

    
  // const categories = async()=>{
  //    const data = await fetch('/api/v1/business-categories');
  //     if (!data.ok) {
  //       throw new Error('Network response was not ok');
  //     }
  //     const result = await data.json();
  //     console.log("hello data", result);
  
  // } 

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
      <section ref={ref} className="w-full">
        <div className="overflow-x-auto bg-[#d9d9d9]">
          <div className="flex justify-between w-full gap-2 px-3 py-1">
            <button
              onClick={() =>{
                // categories()
                handleClick("Categories", "right")
              }}
              className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[6px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454] hover:border-[#1c3454] hover:bg-[#c2c0f5]"
            >
              <BiCategory size={20} />
              Categories
              <FaChevronDown />
            </button>
            <button
              onClick={() =>{
                // businesses()
                handleClick("Shops", "right") 
              } }
              className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[6px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454] hover:border-[#1c3454] hover:bg-[#c2c0f5]"
            >
              <CiShop size={20} />
              Shops
              <FaChevronDown />
            </button>
            <button
              onClick={() => handleClick("Location", "left")}
              className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[6px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454] hover:border-[#1c3454] hover:bg-[#c2c0f5]"
            >
              <CiLocationOn size={20} />
              Location
              <FaChevronDown />
            </button>
            <button
              onClick={() => handleClick("Prices", "left")}
              className="border border-[#edecfe] bg-[#edecfe] rounded-full px-[6px] py-[4px] whitespace-nowrap flex items-center gap-1.5 font-semibold text-[#1c3454] hover:border-[#1c3454] hover:bg-[#c2c0f5]"
            >
              <IoIosPricetag size={20} />
              Prices
              <FaChevronDown />
            </button>
          </div>
        </div>
      </section>
    );
  }
);

export default Classes;
