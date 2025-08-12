import HorizintalDevider from "../common/Dividers/Horizontal-devider";
import Item from "./payment/items";
import BankingDetails from "./payment/bankingDetails";

const Payment: React.FC = () => {
  return (
    <div className="flex flex-col gap-5 w-full lg:w-[100%] p-2">
      <div className="flex flex-col gap-2">
        <span className="font-semibold text-2xl">Shopping Card</span>
        <HorizintalDevider color="bg-gray-300" thickness="h-[1px]" />       
      </div>
      <div className="flex flex-col lg:flex-row gap-6 w-full lg:w-[100%]">
        <Item/>
        <BankingDetails/>        
      </div>

    </div>
  );
};

export default Payment;