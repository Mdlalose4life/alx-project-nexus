
const Login: React.FC= () => {
    return (
        <div className="relative">
                <div className="flex flex-col absolute top-full left-1/2 -translate-x-1/2 lg:w-[220px] mt-2 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-1">
                    <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                        <input 
                            type="text"
                            placeholder="Email:"
                            className="text-sm lg:text-md w-[150px] lg:w-[150px] outline-none"/>
                    </div>
                    <div className="border border-gray-300 rounded-2xl px-[4px] py-[4px]">
                        <input 
                            type="text"
                            placeholder="Password:"
                            className="text-sm lg:text-md w-[150px] lg:w-[150px] outline-none"/>
                    </div>
                    <button className="bg-[#D5D3FD] rounded-2xl text-md" >
                        Login
                    </button>
                    <div className="text-medium flex flex-col items-center gap-1.5">
                        <span>Forgot password ?</span>
                        <p className="text-black">Not registered ? <span className="text-[red]" >Signup</span></p>
                    </div>
                </div>
 
        </div>
    )
}
export default Login
