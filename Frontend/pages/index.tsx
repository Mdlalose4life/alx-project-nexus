import Classes from "@/components/Body/Classes";
import HeroSection from "@/components/Body/HeroSection";
import LeftSideNav from "@/components/Body/responsiveMobileSideNav/leftSideNav";
import RightSideNav from "@/components/Body/responsiveMobileSideNav/rightSideNav";
import SideNav from "@/components/Body/SideNav";
import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";
import ProductCard from "@/components/common/ProductCard";
import { TestProducts } from "@/constants";
import { useEffect, useRef, useState } from "react";

const Home: React.FC = () => {
  const [activePanel, setActivePanel] = useState<"left" | "right"| null>(null)
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const classesRef = useRef<HTMLDivElement>(null);
  const [offsetTop, setOffsetTop] = useState(0);
  const [rightOffset, setRightOffset] = useState(0);
  const [showBackdrop, setShowBackdrop] = useState(false);
  const elementRef = useRef<HTMLDivElement | null>(null);

const handleSetMenuAndPanel = (menu: string, panel: "left" | "right") => {
  setActivePanel(panel);
  setShowBackdrop(true); 

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

useEffect(() => {
  const RightOffset = () => {
    if (elementRef.current) {
      const rect = elementRef.current.getBoundingClientRect();
      const offset = window.innerWidth - rect.right;
      setRightOffset(offset);
    }
  };

  RightOffset();
  window.addEventListener("resize", RightOffset);
  return () => window.removeEventListener("resize", RightOffset);
}, []);

const closeBackdrop = () => {
  setActivePanel(null);
  setActiveMenu(null);
  setShowBackdrop(false);
};

useEffect(() => {
  const handleResize = () => {
    const isMobile = window.innerWidth < 1024;

    if (showBackdrop && isMobile) {
      document.body.classList.add("overflow-hidden");
    } else {
      document.body.classList.remove("overflow-hidden");
    }
  };

  handleResize();
  window.addEventListener("resize", handleResize);

  return () => {
    document.body.classList.remove("overflow-hidden");
    window.removeEventListener("resize", handleResize);
  };
}, [showBackdrop]);

  return (
    <div className="flex flex-col justify-center items-center bg-white p-1">
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
            <section className="flex flex-col w-full lg:w-[85%] bg-[#ececec] p-2 lg:px-6 lg:py-3 rounded-xl overflow-y-auto max-h-[80vh]">
              <ProductCard products={TestProducts}/>
              {showBackdrop && (
                <div
                  onClick={closeBackdrop}
                  className="lg:hidden fixed left-0 right-0 bottom-0 bg-opacity-30 z-40"
                  style={{ 
                    top: `${offsetTop - 160}px`,
                    backgroundColor: "rgba(255, 255, 255, 0.3)",
                    backdropFilter: "blur(2px)" 
                  }}
                />
              )}

              {activePanel === "left" && <LeftSideNav topOffset={offsetTop + 40} rightOffset={rightOffset - 15}/>}
              {activePanel === "right" && <RightSideNav topOffset={offsetTop + 40} />}
              <div className="flex flex-col justify-center items-center pt-3">
                <button className="flex flex-row font-semibold w-[40px] items-center justify-center border-[#edecfe] bg-[#edecfe] px-2.5 rounded-lg hover:border-[#1c3454] hover:bg-[#c2c0f5]"> 
                    More
                </button>
              </div>
          </section>
      </div>
    </div>
  );
};

export default Home;