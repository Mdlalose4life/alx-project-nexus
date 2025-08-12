import { useEffect, useState } from "react";
import { fetchAllMenus, MenuItem } from "@/lib/menuService";
import { useMenu } from "@/store/menuContext";
import HorizintalDevider from "../common/Dividers/Horizontal-devider";

const SideNav: React.FC = () => {
  const { activeMenu } = useMenu();
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
    <aside className="h-full">
      <div className="flex flex-col justify-between p-2">
        <div className="border bg-[#ececec] border-[#ececec] rounded-r-xl min-h-[70%] p-5">
          <h3 className="font-bold mb-1">{activeMenu || "Shop"}</h3>
          <HorizintalDevider color="bg-gray-300" thickness="h-[1.5px]" />

          <div className="flex flex-col space-y-3 max-h-[380px] overflow-y-auto hide-scrollbar lg:pt-1.5">
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

        <div className="mt-4 border bg-[#ececec] border-[#ececec] rounded-r-xl h-[30%] p-5">
          <h5 className="font-semibold mb-1">Filters</h5>
          <HorizintalDevider color="bg-gray-300" thickness="h-[1.5px]" />
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
