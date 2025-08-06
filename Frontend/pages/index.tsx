import Classes from "@/components/Body/Classes";
import HeroSection from "@/components/Body/HeroSection";
import SideNav from "@/components/Body/SideNav";
import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";
import ProductCard from "@/components/common/ProductCard";
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
  return (
    <div className="flex flex-col items-center bg-white p-1">
      <HorizintalDevider thickness="h-[2px]"/>
      <HeroSection/>
      <Classes/>
      <div className="flex flex-row w-full p-1.5">
          <section className="hidden lg:block lg:w-[15%]">
            <SideNav/>
          </section>
            <section className="w-full lg:w-[85%] bg-[#ececec] p-2 lg:px-6 lg:py-3 rounded-xl overflow-y-auto max-h-[80vh]">
              <ProductCard products={TestProducts}/>
              {/* <div>
                <div className="flex flex-col absolute top-66 right-2 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-3">
                    <div className="border bg-white border-[#ececec] rounded-r-xl h-[70%] p-5">
                      <h3 className="font-bold mb-2">Shop</h3>
                      <div className="flex flex-col space-y-3">
                        <span>Incredible Connection</span>
                        <span>Evetech</span>
                        <span>Loot</span>
                        <span>Kilimall</span>
                        <span>TechSmart</span>
                      </div>
                    </div>
                    <HorizintalDevider/>
                   <div className="mt-4 border bg-white border-[#ececec] rounded-r-xl  h-[30%] p-5">
                    <h5 className="font-semibold mb-1">Filters</h5>
                    <div className="flex flex-col space-y-3">
                      <span>High to Low</span>
                      <span>Low to High</span>
                    </div>
                  </div>
                </div>
              </div> */}

              {/* <div>
                <div className="flex flex-col absolute top-66 right-34 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-3">
                    <div className="border bg-white border-[#ececec] rounded-l-xl h-[70%] p-5">
                      <h3 className="font-bold mb-2">Shop</h3>
                      <div className="flex flex-col space-y-3">
                        <span>Incredible Connection</span>
                        <span>Evetech</span>
                        <span>Loot</span>
                        <span>Kilimall</span>
                        <span>TechSmart</span>
                      </div>
                    </div>
                    <HorizintalDevider/>
                   <div className="mt-4 border bg-white border-[#ececec] rounded-l-xl  h-[30%] p-5">
                    <h5 className="font-semibold mb-1">Filters</h5>
                    <div className="flex flex-col space-y-3">
                      <span>High to Low</span>
                      <span>Low to High</span>
                    </div>
                  </div>
                </div>
              </div> */}
          </section>
      </div>
    </div>
  );
};

export default Home;