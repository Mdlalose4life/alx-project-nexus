
const Signup: React.FC = () => {
    return (
        <div className="relative">
                <div className="flex flex-col absolute top-full left-1/2 -translate-x-[93%] w-[230px] lg:w-[270px] mt-2 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-1">
                    <div className="rounded-2xl px-[2px] py-[2px]">
                        <input 
                            type="text"
                            placeholder="Email: "
                            className="text-md w-[190px] rounded-2xl border border-gray-400 bg-purple-50 text-gray-500 lg:w-full p-1.5 px-2 outline-none"/>
                    </div>
                    <div className="rounded-2xl px-[4px] py-[4px]">
                        <input 
                            type="text"
                            placeholder="Password:"
                            className="text-md w-[190px] rounded-2xl border border-gray-400 bg-purple-50 text-gray-500 lg:w-full p-1.5 px-2 outline-none"/>
                    </div>
                    <div className="rounded-2xl px-[2px] py-[2px]">
                        <input 
                            type="text"
                            placeholder="Comfirm Password:"
                            className="text-md w-[190px] rounded-2xl border border-gray-400 bg-purple-50 text-gray-500 lg:w-full p-1.5 px-2 outline-none"/>
                    </div>
                    <button className="bg-[#D5D3FD] rounded-2xl" >Sign Up</button>
                    <div className="text-sm lg:text-md flex flex-col items-center">
                        <p className="text-black">Registered ? <span className="text-[red]" >Login</span></p>
                    </div>
                </div>
            </div>

    )
}
export default Signup;