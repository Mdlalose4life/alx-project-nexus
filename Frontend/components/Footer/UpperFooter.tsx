import FooterElements from "../Footer/Footer";

const UpperFooter: React.FC = () => {
  return (
    <div className="flex flex-col">
        <div className="">
            <img src="Images/Logo.png" alt="Lower Logo" className="w-[130px]"/>
        </div>
        <div className="pl-11.5">
            <div className="flex flex-wrap lg:flex-nowrap lg:justify-center text-[#1c3454] text-[12px] lg:text-[16px] gap-[60px] lg:gap-60">
                <div className="flex flex-col gap-[9px] lg:gap-5">
                    <h3 className="font-semibold">Explore</h3>
                    <p>TVs on Sale</p>
                    <p>Radios Collection</p>
                    <p>TNew Arrivals</p>
                    <p>Deals & Discounts</p>
                    <p>Become a Seller</p>
                </div>
                <div className="flex flex-col gap-[9px] lg:gap-5">
                    <h3 className="font-semibold">Stores</h3>
                        <p>Stores in Johannesburg</p>
                        <p>Stores in Cape Town</p>
                        <p> Featured Sellers</p>
                        <p> Verified Partners</p>
                        <p>Store Directory</p>     
                </div>
                <div className="flex flex-col gap-[9px] lg:gap-5">
                    <h3 className="font-semibold">Help</h3>
                    <p>How It Works</p>
                    <p>Track Your Order</p>
                    <p>Cancel or Modify Order</p>
                    <p>Refund Policy</p>
                    <p>Contact Support</p>
                    <p>FAQs</p>
                </div>
                <div className="flex flex-col gap-[9px] lg:gap-5">
                    <h3 className="font-semibold">Company</h3>
                    <p>About Us</p>
                    <p>Careers</p>
                    <p>Press</p>
                    <p>Advertise With Us</p>
                    <p>Our Mission</p>
                    <p>Partners</p>
                </div>
            </div>
        </div>
    </div>
  );
};

export default UpperFooter;
