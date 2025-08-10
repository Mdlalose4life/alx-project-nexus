import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider"
import { fetchAllMenus, MenuItem } from "@/lib/menuService";
import { useMenu } from "@/store/menuContext";
import { useEffect, useState } from "react";

// const  TestMenu = [
//   {
//     name: "Categories",
//     items: {
//     item1: "Clothing",
//     item2: "Kitchen",
//     item3: "Electronics",
//     item4: "Beauty & Personal Care",
//     item5: "Home Appliances",
//     item6: "Furniture",
//     item7: "Toys & Games",
//     item8: "Automotive",
//     item9: "Books",
//     item10: "Sports & Outdoors",
//     item11: "Groceries",
//     item12: "Health & Wellness",
//     item13: "Pet Supplies",
//     item14: "Jewelry",
//     item15: "Watches",
//     item16: "Bags & Luggage",
//     item17: "Baby Products",
//     item18: "Office Supplies",
//     item19: "Garden & Tools",
//     item20: "Musical Instruments",
//     },
//   },
//   {
//     name: "Shops",
//     items: {
//       item1: "Incredible Connection",
//       item2: "Evetech",
//       item3: "Loot",
//       item4: "Kilimall",
//       item5: "TechSmart",
//     },
//   },
//   {
//     name: "Location",
//     items: {
//       item1: "Johannesburg",
//       item2: "Cape Town",
//       item3: "Pretoria",
//       item4: "Durban",
//       item5: "Newcastle",
//     },
//   },
//   {
//     name: "Prices",
//     items: {
//       item1: "0 - 2k",
//       item2: "2k - 4k",
//       item3: "4k - 6k",
//     },
//   },
// ];

interface ActiveProps {
  topOffset?: number;
  rightOffset?:number
}
const LeftSideNav: React.FC<ActiveProps> = ({ topOffset, rightOffset}) => {
  const { activeMenu} = useMenu()
  const [menuData, setMenuData] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMenus = async () => {
      try {
        const menus = await fetchAllMenus();
        setMenuData(menus);
      } catch (error) {
        console.error("Error fetching menus:", error);
      } finally {
        setLoading(false);
      }
    };

    loadMenus();
  }, []);

  const selected = menuData.find((menu) => menu.name === activeMenu);

    return (
            <div className="inset-0 z-50 lg:hidden">
                <div className="lg:hidden block flex-col absolute top-[37%] z-40 bg-[#EDECFE] text-black p-4 rounded-xl gap-3"
                    style={{ top: `${topOffset}px` , left: `${rightOffset}`}}
                >
                    <div className="border bg-[#c2c0f5]  border-[#ececec] rounded-l-xl h-[70%] p-5">
                        <h3 className="font-bold mb-2">{ activeMenu || "Shop"}</h3>
                        <HorizintalDevider color="bg-gray-300" thickness="h-[1.5px]"/>
                        <div className="flex flex-col space-y-3 max-h-[300px] overflow-y-auto hide-scrollbar lg:pt-1.5">
                          {loading ? (
                            <span className="text-sm text-gray-500">Loading...</span>
                          ) : selected ? (
                            Object.values(selected.items).map((item, idx) => (
                              <span
                                className="hover:bg-[#c2c0f5] rounded-full p-2 text-sm w-[150px]"
                                key={idx}
                              >
                                {item}
                              </span>
                            ))
                          ) : (
                            <span className="text-sm text-gray-500">No items found</span>
                          )}
                        </div>
                    </div>
                    <HorizintalDevider color="bg-gray-300"/>
                    <div className="mt-4 border bg-[#c2c0f5] border-[#ececec] rounded-l-xl  h-[30%] p-5">
                    <h5 className="font-semibold mb-1">Filters</h5>
                    <div className="flex flex-col space-y-3">
                        <span>High to Low</span>
                        <span>Low to High</span>
                    </div>
                    </div>
                </div>
            </div> 
    )
}
export default LeftSideNav