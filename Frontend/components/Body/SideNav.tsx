'use client';
import React from 'react';


const SideNav: React.FC = () => {
  
    const categories = async()=>{
     const data = await fetch('/api/v1/business-categories');
      if (!data.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await data.json();
      console.log("hello data", result);
      return result;
  } 
  return (
    <aside className="h-full">
      <div className="flex flex-col justify-between h-full p-2">
        <div className="border bg-[#ececec] border-[#ececec] rounded-r-xl h-[70%] p-5">
          <h3 className="font-bold mb-2">Shop</h3>
          <div className="flex flex-col space-y-3">
            <span>Incredible Connection</span>
            <span>Evetech</span>
            <span>Loot</span>
            <span>Kilimall</span>
            <span>TechSmart</span>
          </div>
        </div>

        <div className="mt-4 border bg-[#ececec] border-[#ececec] rounded-r-xl  h-[30%] p-5">
          <h5 className="font-semibold mb-1">Filters</h5>
          <div className="flex flex-col space-y-3">
            <span>High to Low</span>
            <span>Low to High</span>
          </div>
        </div>
        <button className=" border-2"onClick={()=>{categories()}}>categories</button>
      </div>
    </aside>
  );
};

export default SideNav;
