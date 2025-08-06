import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider";
import Image from "next/image";
import { useState } from "react";
import { CiShop } from "react-icons/ci";
import { FaStar, FaRegStar } from "react-icons/fa";
import { PiShoppingBag, PiShoppingCart } from "react-icons/pi";

const ProductDetailsPage: React.FC = () => {
  const [mainImage, setMainImage] = useState("/Images/productG.jpeg");

  const thumbnailImages = [
    "/Images/productG.jpeg",
    "/Images/productG.jpeg",
    "/Images/productG.jpeg",
    "/Images/productG.jpeg",
    "/Images/productG.jpeg",
  ];

  return (
    <div className="p-4 md:p-8 w-full">
      <h1 className="lg:text-xl font-semibold lg:text-center lg:mb-6 lg:mr-90">LG OLED evo C3 4K Smart TV</h1>
      <div className="flex flex-col lg:flex-row gap-10">
        <div>
            <div className="flex flex-col lg:flex-row gap-4 flex-1">
                <div className="flex lg:flex-col gap-2 overflow-y-auto max-h-[70vh] lg:overflow-visible">
                    {thumbnailImages.map((src, index) => (
                    <Image
                        key={index}
                        src={src}
                        alt="thumbnail"
                        width={100}
                        height={100}
                        className="border border-gray-300 rounded cursor-pointer"
                        onClick={() => setMainImage(src)}
                    />
                    ))}
                    <div className="w-[80px] h-[100px] flex items-center justify-center border rounded bg-gray-100 text-sm">
                    +5
                    </div>
                </div>
                <div className="flex justify-center items-center rounded w-full lg:w-[700px] h-auto">
                    <Image
                    src={mainImage}
                    alt="Product"
                    width={500}
                    height={400}
                    className="object-contain"
                    />
                </div>
            </div>
            <div className="flex justify-center mt-4 gap-3">
                <button className="flex flex-row items-center bg-[#c3c1fb] text-black px-4 py-1 rounded-full font-semibold hover:bg-[#a3a1f8] gap-3">
                  <PiShoppingCart size={30}/>
                    Add To Cart
                </button>
                <button className="flex flex-row items-center bg-[#c3c1fb] text-black px-4 py-1 rounded-full font-semibold hover:bg-[#a3a1f8] gap-3">
                    <CiShop size={30}/>
                    Shop
                </button>
            </div>
        </div>

        <div className="bg-[#f5f4fe] border border-gray-200 rounded-3xl p-6 w-full lg:w-[50%] text-center">
          <h2 className="font-semibold mb-2">Review</h2>
          <p className="text-sm mb-2">LG OLED evo C3 4K Smart TV</p>
          <div className="flex justify-center bg-white rounded-4xl text-6xl">
            <img src="/Images/review.png" alt="Reviews" className="h-[520px]" />
          </div>
            <p className="mt-4 text-gray-500">
             No Review Yet
            </p>
        </div>
      </div>
      <div className="mt-2 lg:w-[60%]">
        <h2 className="text-lg font-semibold mb-2">Description</h2>
        <HorizintalDevider/>
        <p className="text-sm text-gray-700 leading-relaxed mb-8">
            The LG OLED evo C3 4K Smart TV is a premium television designed for immersive entertainment, 
            blending stunning picture quality with intelligent features. Powered by LG’s α9 AI Processor Gen,
            it delivers breathtaking visuals with self-lit OLED evo technology—producing perfect blacks, vibran
            t colors, and exceptional contrast. Whether you're streaming movies, gaming, or browsing content,
            its 120Hz refresh rate, Dolby Vision, Dolby Atmos, and advanced gaming features like NVIDIA
            G-Sync and FreeSync make every experience smooth and lifelike. With webOS 23 and ThinQ AI, 
            users enjoy a personalized smart interface with voice control and seamless smart home integration.
            Sleek and minimalist, the LG C3 fits beautifully in any modern space, making it an ideal centerpiece 
            for both tech lovers and design-conscious viewers.
        </p>
      </div>
    <HorizintalDevider/>
      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-2">Key Features</h2>
        <ul className="text-sm list-disc list-inside text-gray-700 space-y-2">
          <li>Self-Lit OLED evo Panel (4K UHD, 3840 × 2160): Delivers perfect blacks, infinite contrast, and vibrant color  volume with 100% fidelity Reddit+7gp1qa.lg.com+7DID Electrical+7goodluckafrica.com+1LG Electronics+1.</li>
          <li>α9 AI Processor Gen6: Uses AI-powered upscaling, noise reduction, and genre‑adaptive tuning to optimize both image and sound in real time LG Electronics+7DID Electrical+7goodluckafrica.com+7.</li>
          <li>Brightness Booster: Enhanced brightness ensures clear, high-contrast visuals even in well-lit rooms LG Electronics+4Amazon South Africa+4Reddit+4.webOS 23 with ThinQ AI:</li>
          <li>Navigate easily with Quick Cards, tailored profiles, and built‑in AI voice assistants (Alexa, Google Assistant, Apple HomeKit) DID Electrical+10Amazon South Africa+10Len Wallis Audio+10.</li>
          <li>Dolby Vision & Atmos: Supports Dolby Vision HDR, HDR10 Pro, and HLG; AI Sound Pro creates a virtual 9.1.2 surround‑sound experience through Dolby Atmos integration Elecmert Solutions+9Len Wallis Audio+9goodluckafrica.com+9.</li>
          <li>Ultimate Gaming Setup: 120Hz refresh, HDMI 2.1 ports, etc.</li>
        </ul>
      </div>
    </div>
  );
};

export default ProductDetailsPage;
