import { CiCircleMore } from "react-icons/ci";
const More: React.FC = () => {
    return (
        <div className="p-[6px]">
            <CiCircleMore size={30}/>
            {/* <div className="flex flex-col absolute top-12.6 right-0 z-50 bg-[#EDECFE] text-black p-4 rounded-xl">
                <button>Sign in</button>
                <button>Sign Up</button>
            </div> */}
            {/* <div className="flex flex-col absolute top-12.6 right-0 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-1">
                <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                    <input 
                        type="text"
                        placeholder="Email:"
                        className="text-sm w-[150px] outline-none"/>
                </div>
                <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                    <input 
                        type="text"
                        placeholder="Password:"
                        className="text-sm w-[150px] outline-none"/>
                </div>
                <button className="bg-[#D5D3FD] rounded-2xl" >Sign Up</button>

                <div className="text-sm flex flex-col items-center">
                    <p className="text-black">Not registered <span className="text-[red]" >SignIn</span></p>
                </div>
            </div> */}

            {/* <div className="flex flex-col absolute top-12.6 right-0 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-1">
                <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                    <input 
                        type="text"
                        placeholder="Email:"
                        className="text-sm w-[150px] outline-none"/>
                </div>
                <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                    <input 
                        type="text"
                        placeholder="Password:"
                        className="text-sm w-[150px] outline-none"/>
                </div>
                <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                    <input 
                        type="text"
                        placeholder="Comfirm Password:"
                        className="text-sm w-[150px] outline-none"/>
                </div>
                <button className="bg-[#D5D3FD] rounded-2xl" >Sign Up</button>
                <div className="text-sm flex flex-col items-center">
                    <p className="text-black">Registered <span className="text-[red]" >SignIn</span></p>
                </div>
            </div> */}

        </div>
    )
}
export default More