import { useState } from "react";
import { CiCircleMore } from "react-icons/ci";
import { GoSignIn } from "react-icons/go";
import { CiLogin } from "react-icons/ci";
import Login from "./More/login";
import Signup from "./More/Signup";

interface MoreProp {
    activeView: string | null;
    setActiveView: (view: "Cart" | "Profile" | "More" | null) => void;
}

const More: React.FC<MoreProp> = ({activeView, setActiveView}) => {
    const isOpen = activeView === "More";

    const [moreView, setMoreView] = useState<"menu" | "signin" | "signup" | null>(null);

    const toggleMore = () => {
        setActiveView(isOpen ? null : "More")
        setMoreView("menu")
    }
    return (
        <div className="p-[4px]">
            <div className="relative inline-block">
                <button
                onClick={toggleMore}
                className="p-[6px] hover:scale-105 transform transition-transform duration-300 cursor-pointer"
                >
                <CiCircleMore size={30} />
                </button>

                {isOpen && moreView === "menu" && (
                <div className="flex flex-col absolute top-full left-1/2 -translate-x-[86%] mt-2 w-[120px] lg:w-[120px] gap-5 bg-[#EDECFE] text-black p-4 rounded-xl shadow-xl z-20">
                    <div className="flex flex-row items-center justify-center gap-2.5">
                        <button 
                        className="flex flex-row justify-center items-center gap-3.5 font-semibold lg:text-md bg-[#D5D3FD] rounded-2xl py-2 w-full text-sm hover:bg-[#c2c0f5] transition-colors"
                        onClick={() => setMoreView("signin")}>
                            <GoSignIn/>
                            Login
                        </button>
                    </div>
                    <div className="flex flex-row items-center justify-center gap-2.5">
                        <button 
                        className="flex flex-row justify-center items-center gap-3.5 font-semibold lg:text-md bg-[#D5D3FD] rounded-2xl py-2 w-full text-sm hover:bg-[#c2c0f5] transition-colors"
                        onClick={() => setMoreView("signup")}>
                            <CiLogin />
                            Sign Up
                        </button>
                    </div>
                </div>
                )}
            </div>

        {moreView === "signin" && (
            <Login />
        )}

        {moreView === "signup" && (
            <Signup />
        )}
        </div>
  );
};

export default More;
