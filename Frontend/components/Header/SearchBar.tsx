import { useEffect, useState } from "react";
import { CiSearch } from "react-icons/ci";
const SearchBar: React.FC = () => {
    const [innerWindow, setInnerWindow] = useState<number | null>(null);

    useEffect(()=> {
      const handleResize = () => {
        setInnerWindow(window.innerWidth);
      }

      handleResize()
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }, [])
    


    const renderResponsiveComponent = () => {
              if (innerWindow == null) return null

      if (innerWindow <= 600) {
        return <div className="flex flex-row items-center border-1 border-[#D9D9D9] bg-[#D9D9D9] rounded-full gap-2.5 px-1 py-2">
            <CiSearch size={30}/>
            <input
            type="text"
            placeholder="Search"
            className="w-[100px] outline-none"
            />
        </div>;
      } else if (innerWindow <= 1200) {
        return <div className="flex flex-row items-center border-1 border-[#D9D9D9] bg-[#D9D9D9] rounded-full gap-2.5 px-1 py-2">
            <CiSearch size={30}/>
            <input
            type="text"
            placeholder="Search For a Product, Category, Shop..."
            className="w-[300px] outline-none"
            />
        </div>;
      } else {
        return <div className="flex flex-row items-center border-1 border-[#D9D9D9] bg-[#D9D9D9] rounded-full gap-2.5 px-1 py-1.5">
            <CiSearch size={30}/>
            <input
            type="text"
            placeholder="Search For a Product, Category, Shop..."
            className="w-[500px] outline-none"
            />
        </div>;
      }
    }
    

    return (
        <div>
            {renderResponsiveComponent()}
        </div>
    )
}
export default SearchBar