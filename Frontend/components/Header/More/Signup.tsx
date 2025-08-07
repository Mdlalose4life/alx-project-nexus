
const Signup: React.FC = () => {
    return (
        <div className="relative">
                <div className="flex flex-col absolute top-full left-1/2 -translate-x-[93%] mt-2 z-50 w-[250px] bg-[#EDECFE] text-black p-4 rounded-xl gap-1">
                    <div className="border border-gray-300 rounded-2xl px-[2px] py-[2px]">
                        <input 
                            type="text"
                            placeholder="Email: "
                            className="text-sm lg:text-md rounded-lg  w-[200px] outline-none"/>
                    </div>
                    <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                        <input 
                            type="text"
                            placeholder="Password:"
                            className="text-sm lg:text-md rounded-lg  w-[200px] outline-none"/>
                    </div>
                    <div className="border border-gray-300 rounded-2xl px-[2px] py-[2px]">
                        <input 
                            type="text"
                            placeholder="Comfirm Password:"
                            className="text-sm lg:text-md rounded-lg  w-[200px] outline-none"/>
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