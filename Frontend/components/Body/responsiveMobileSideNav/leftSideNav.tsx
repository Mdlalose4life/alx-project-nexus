import HorizintalDevider from "@/components/common/Dividers/Horizontal-devider"
interface ActiveProps {
  activeMenu: string | null;
  topOffset?: number;
}
const LeftSideNav: React.FC<ActiveProps> = ({activeMenu, topOffset}) => {
    return (
        <div>
            <div className="lg:hidden block flex-col absolute top-[37%] right-48 z-50 bg-[#EDECFE] text-black p-4 rounded-xl gap-3"
                style={{ top: `${topOffset}px` }}
            >
                <div className="border bg-white border-[#ececec] rounded-l-xl h-[70%] p-5">
                    <h3 className="font-bold mb-2">{activeMenu}</h3>
                    <div className="flex flex-col space-y-3">
                    <span>Sbu</span>
                    <span>Sbu</span>
                    <span>Sbu</span>
                    <span>Sbu</span>
                    <span>Sbu</span>
                    </div>
                </div>
                <HorizintalDevider color="bg-gray-300"/>
                <div className="mt-4 border bg-white border-[#ececec] rounded-l-xl  h-[30%] p-5">
                <h5 className="font-semibold mb-1">Filters</h5>
                <div className="flex flex-col space-y-3">
                    <span>High to Low</span>
                    <span>Low to High</span>
                </div>
                </div>
            </div>
        </div>
    )
}
export default LeftSideNav