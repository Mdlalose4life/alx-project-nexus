import { PiShoppingCartLight } from "react-icons/pi";
const Cart: React.FC = () => {
    return (
        <div className="p-[6px]">
            <PiShoppingCartLight size={30} />
            {/* <div className="flex flex-col absolute top-12.6 right-15 z-50 bg-[#EDECFE] text-black p-4 rounded-xl">
                <div className="flex flex-row gap-x-0.5">
                    <div>
                        <img 
                        src="/Images/productA.webp"
                        alt="Cart Product"
                        className="h-[40px]"/>
                    </div>
                    <div className="">
                        <h3>LG OLED</h3>
                        <span>R 1200</span>
                    </div>
                </div>
                <button className="bg-[#D5D3FD] rounded-2xl">
                    Checkout
                </button>
            </div> */}
        </div>
    )
}
export default Cart