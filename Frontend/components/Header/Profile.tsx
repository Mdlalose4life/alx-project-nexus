import { CgProfile } from "react-icons/cg";

interface ProfileProp {
  activeView: string | null;
  setActiveView: (view: "Cart" | "Profile" | "More" | null) => void;
}

const Profile: React.FC<ProfileProp> = ({ activeView, setActiveView }) => {
  const isOpen = activeView === "Profile";

  const toggleProfile = () => {
    setActiveView(isOpen ? null : "Profile");
  };

  return (
    <div className="relative">
      <button
        onClick={toggleProfile}
        className="p-[4px] hover:scale-105 transform transition-transform duration-300 cursor-pointer"
      >
        <CgProfile size={30} />
      </button>

      {isOpen && (
        <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-[130px] lg:w-[150px] bg-[#EDECFE] text-black p-1 lg:p-4 rounded-xl shadow-xl z-50">
          <button className="flex flex-row justify-center items-center gap-3.5 font-semibold lg:text-md bg-[#D5D3FD] rounded-2xl py-2 w-full text-sm hover:bg-[#c2c0f5] transition-colors">
            <CgProfile size={35} />
            Profile
          </button>
        </div>
      )}
    </div>
  );
};

export default Profile;
