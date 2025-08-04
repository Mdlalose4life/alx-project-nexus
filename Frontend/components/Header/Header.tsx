import Cart from "./Cart";
import More from "./More";
import Profile from "./Profile";
import SearchBar from "./SearchBar";

const MainHeader: React.FC = () => {
  return (
    <div className="bg-[#F5F5F5] w-full">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center">
            <img 
            src="/Images/Logo.png"
            className="w-[100px] lg:w-[150px]"
            />
        </div>
            <div>
              <SearchBar/>
          </div>
        <nav className="flex flex-row items-center">
            <Cart/>
            <Profile/>
            <More/>
        </nav>
      </div>
    </div>
  );
}

export default MainHeader;