import Classes from "@/components/Body/Classes";
import HeroSection from "@/components/Body/HeroSection";
import LeftSideNav from "@/components/Body/responsiveMobileSideNav/leftSideNav";
import RightSideNav from "@/components/Body/responsiveMobileSideNav/rightSideNav";
import SideNav from "@/components/Body/SideNav";
import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";
import ProductCard from "@/components/common/ProductCard";
import { useEffect, useRef, useState } from "react";
const TestProducts = [
  {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },   {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  },
    {
    id: 1,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product A description.",
    price: 19.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 2,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product B description.",
    price: 29.99,
    image: "Images/productH.png",
  },
  {
    id: 4,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productD.webp",
  },
    {
    id: 5,
    name: "Samsung Crystal UHD 4K...",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productE.webp",
  },
  {
    id: 6,
    name: "TCL QLED 4K Google TV",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productF.png",
  },
  {
    id: 7,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
    {
    id: 8,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productG.jpeg",
  },
  {
    id: 9,
    name: "Sinotec 43-Inch Smart LED",
    description: "This is product C description.",
    price: 39.99,
    image: "Images/productH.png",
  }
];


const Home: React.FC = () => {
  const [activePanel, setActivePanel] = useState<"left" | "right"| null>(null)
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const classesRef = useRef<HTMLDivElement>(null);
  const [offsetTop, setOffsetTop] = useState(0);

const handleSetMenuAndPanel = (menu: string, panel: "left" | "right") => {
  setActiveMenu(menu);
  setActivePanel(panel);

  requestAnimationFrame(() => {
    if (classesRef.current) {
      const offset = classesRef.current.offsetTop;
      setOffsetTop(offset);

      classesRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
};



  return (
    <div className="flex flex-col items-center bg-white p-1">
      <HorizintalDevider thickness="h-[2px]"/>
      <HeroSection/>
      <Classes 
        ref={classesRef}
        setActiveMenu={(menu) => handleSetMenuAndPanel(menu, activePanel!)}
        setActivePanel={(panel) => setActivePanel(panel)}
      />
      <div className="flex flex-row w-full p-1.5">
          <section className="hidden lg:block lg:w-[15%]">
            <SideNav/>
          </section>
            <section className="w-full lg:w-[85%] bg-[#ececec] p-2 lg:px-6 lg:py-3 rounded-xl overflow-y-auto max-h-[80vh]">
              <ProductCard products={TestProducts}/>
              {activePanel === "left" && <LeftSideNav activeMenu={activeMenu} topOffset={offsetTop + 40}/>}
              {activePanel === "right" && <RightSideNav activeMenu={activeMenu} topOffset={offsetTop + 40} />}
          </section>
      </div>
    </div>
  );
};

export default Home;