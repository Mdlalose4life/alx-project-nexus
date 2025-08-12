import UpperFooter from "./UpperFooter";
import LowerFooter from "./LowerFooter";

const Footer: React.FC = () => {
  return (
    <footer className="bg-[#d9d9d9] py-6">
      <div className="bg-[#d9d9d9">
        <UpperFooter/>
      </div>
      <div className="bg-[white]">
        <LowerFooter/>
      </div>
    </footer>
  );
};

export default Footer;
