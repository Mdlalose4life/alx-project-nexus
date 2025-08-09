import { useMenu } from "@/store/MenuContext";
import HorizintalDevider from "../common/Dividers/Horizontal-devider";

const  TestMenu = [
  {
    name: "Categories",
    items: {
    item1: "Clothing",
    item2: "Kitchen",
    item3: "Electronics",
    item4: "Beauty & Personal Care",
    item5: "Home Appliances",
    item6: "Furniture",
    item7: "Toys & Games",
    item8: "Automotive",
    item9: "Books",
    item10: "Sports & Outdoors",
    item11: "Groceries",
    item12: "Health & Wellness",
    item13: "Pet Supplies",
    item14: "Jewelry",
    item15: "Watches",
    item16: "Bags & Luggage",
    item17: "Baby Products",
    item18: "Office Supplies",
    item19: "Garden & Tools",
    item20: "Musical Instruments",
    },
  },
  {
    name: "Shops",
    items: {
      item1: "Incredible Connection",
      item2: "Evetech",
      item3: "Loot",
      item4: "Kilimall",
      item5: "TechSmart",
    },
  },
  {
    name: "Location",
    items: {
      item1: "Johannesburg",
      item2: "Cape Town",
      item3: "Pretoria",
      item4: "Durban",
      item5: "Newcastle",
    },
  },
  {
    name: "Prices",
    items: {
      item1: "0 - 2k",
      item2: "2k - 4k",
      item3: "4k - 6k",
    },
  },
];


const SideNav: React.FC = () => {
  const { activeMenu } = useMenu()
  const selected = TestMenu.find(menu => menu.name === activeMenu);

  return (
    <aside className="h-full">
      <div className="flex flex-col justify-between p-2">
        <div className="border bg-[#ececec] border-[#ececec] rounded-r-xl min-h-[70%] p-5">
          <h3 className="font-bold mb-1">{activeMenu || "Shop"}</h3>
          <HorizintalDevider color="bg-gray-300" thickness="h-[1.5px]"/>
          <div className="flex flex-col space-y-3 max-h-[380px] overflow-y-auto hide-scrollbar lg:pt-1.5">
            { selected 
            ? Object.values(selected.items).map((item, idx) => (
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]" key={idx}>
                {item}
              </span>
            ))
             : (
              <>
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]" >Incredible Connection</span>
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">Evetech</span>
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">Loot</span>
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">Kilimall</span>
              <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">TechSmart</span>
             </>
             )}
          </div>
        </div>
        <div className="mt-4 border bg-[#ececec] border-[#ececec] rounded-r-xl  h-[30%] p-5">
          <h5 className="font-semibold mb-1">Filters</h5>
            <HorizintalDevider color="bg-gray-300" thickness="h-[1.5px]"/>
          <div className="flex flex-col space-y-3 lg:pt-1.5">
            <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">High to Low</span>
            <span className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]">Low to High</span>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default SideNav;
