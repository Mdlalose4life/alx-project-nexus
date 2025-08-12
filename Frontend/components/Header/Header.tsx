import { useEffect, useRef, useState } from "react";
import Cart from "./Cart";
import More from "./More";
import Profile from "./Profile";
import SearchBar from "./SearchBar";
import Link from "next/link";
import Image from "next/image";

const MainHeader: React.FC = () => {
  const [activeView, setActiveView] = useState<"Cart" | "Profile" | "More" | null>(null);
  const headerRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        headerRef.current &&
        !headerRef.current.contains(event.target as Node)
      ) {
        setActiveView(null);
      }
    };

    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <div className="bg-[#F5F5F5] w-full">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/">
          <div className="flex items-center">
            <Image src="/Images/Logo.png" width={120} height={80} alt="Footer-logo" className="w-[100px] lg:w-[120px]" />
          </div>
        </Link>

        <div>
          <SearchBar />
        </div>

        <nav ref={headerRef} className="flex flex-row items-center lg:gap-8">
          <Cart activeView={activeView} setActiveView={setActiveView} />
          <Profile activeView={activeView} setActiveView={setActiveView} />
          <More activeView={activeView} setActiveView={setActiveView} />
        </nav>
      </div>
    </div>
  );
};

export default MainHeader;
